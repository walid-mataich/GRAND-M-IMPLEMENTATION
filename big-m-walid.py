import numpy as np
from tabulate import tabulate
from scipy.optimize import linprog

def afficher_premier_tableau(c_grand_m, A_grand_m, b):
    
    # Créer les en-têtes
    num_vars = A_grand_m.shape[1]
    headers = ["b"] + [f"x{i+1}" for i in range(num_vars)]

    # Construire les lignes du tableau
    tableau = np.hstack([b.reshape(-1, 1), A_grand_m])  
    tableau = tableau.tolist()

    # Ajouter la ligne des coûts 
    tableau.append(["z"] + list(c_grand_m))  

    # Afficher avec tabulate
    print("\n----- Premier Tableau -----")
    print(tabulate(tableau, headers=headers, tablefmt="fancy_grid"))
    print("-------------------------------\n")


def GrandM(c, A, b, c_signe, M=1000):

    num_cons, num_vars = A.shape
    A_grand_m = A.copy()
    c_grand_m = np.copy(c)
    s_vars = []
    a_vars = []

    for i, ct in enumerate(c_signe):
        if ct == '<=':
            # Ajouter une variable d'écart 
            s_col = np.zeros((num_cons,))
            s_col[i] = 1
            s_vars.append(len(c_grand_m))  
            c_grand_m = np.hstack([c_grand_m, 0])  # Coût de la variable d'écart = 0
            A_grand_m = np.hstack([A_grand_m, s_col.reshape(-1, 1)])
        
        elif ct == '>=':
            # Ajouter une variable d'excès(avec cout = coeff = -1)  et une variable artificielle
            e_col = np.zeros((num_cons,))
            e_col[i] = -1  
            a_col = np.zeros((num_cons,))
            a_col[i] = 1  

            c_grand_m = np.hstack([c_grand_m, 0, M])  # Coût excess = 0, artificielle = M
            A_grand_m = np.hstack([A_grand_m, e_col.reshape(-1, 1), a_col.reshape(-1, 1)])
            a_vars.append(len(c_grand_m) - 1)  
        elif ct == '=':
            # Ajouter une variable artificielle
            a_col = np.zeros((num_cons,))
            a_col[i] = 1  # Variable artificielle

            c_grand_m = np.hstack([c_grand_m, M])  # Coût de la variable artificielle = M
            A_grand_m = np.hstack([A_grand_m, a_col.reshape(-1, 1)])
            a_vars.append(len(c_grand_m) - 1)  
    
    afficher_premier_tableau(c_grand_m, A_grand_m, b)
    # Résolution avec linprog
    result = linprog(c_grand_m, A_eq=A_grand_m, b_eq=b, method='simplex')

    print(result) #afficher le resultat

    # Retourner la solution finale sans les variables artificielles et d'excès
    final_solution = result.x[:num_vars]
    return final_solution, result.fun

# Exemple
if __name__ == "__main__":
   
   #coefficients de la fnct objectif
    c = [-2, -3]  

    # Contraintes
    A = np.array([
        [1, 2],    
        [2, 1]    
    ])
    b = np.array([8, 6])
    c_signe = ['<=', '>=']  # Types des contraintes

    # Résolution
    solution, optimal_value = GrandM(c, A, b, c_signe)

    print("Solution optimale:")

    for i in range(len(solution)):
        
        print(f"x{i+1} = {solution[i]}")

    print("Valeur optimale de z:", -optimal_value)  # Négation pour le problème de maximisation
