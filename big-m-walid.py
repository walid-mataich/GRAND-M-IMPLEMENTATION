import numpy as np
from tabulate import tabulate
from scipy.optimize import linprog

def afficher_premier_tableau(c_grand_m, A_grand_m, b):
    
    # LES EN-TETES
    num_vars = A_grand_m.shape[1]
    headers = ["b"] + [f"x{i+1}" for i in range(num_vars)]

    # LES LIGNES DU TABLEAU
    tableau = np.hstack([b.reshape(-1, 1), A_grand_m])  
    tableau = tableau.tolist()

    # LA LIGNE DES COUTS
    tableau.append(["z"] + list(c_grand_m))  

    # AFFICHER LE TABLEAU
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
            # AJOUTER UNE VARIABLE D'ECART
            s_col = np.zeros((num_cons,))
            s_col[i] = 1
            s_vars.append(len(c_grand_m))  
            c_grand_m = np.hstack([c_grand_m, 0])  # COUT DE S = 0
            A_grand_m = np.hstack([A_grand_m, s_col.reshape(-1, 1)])
        
        elif ct == '>=':
            # SOUSTRAIRE UNE VARIABLE D'EXCES ET AJOUTER UN VARIABLE ARTIFICIELLE
            e_col = np.zeros((num_cons,))
            e_col[i] = -1  
            a_col = np.zeros((num_cons,))
            a_col[i] = 1  

            c_grand_m = np.hstack([c_grand_m, 0, M])  # COUT DE E= 0, COUT DE A = M
            A_grand_m = np.hstack([A_grand_m, e_col.reshape(-1, 1), a_col.reshape(-1, 1)])
            a_vars.append(len(c_grand_m) - 1)  
        elif ct == '=':
            # AJOUT D'UNE VARIABLE ARTIFICIELLE
            a_col = np.zeros((num_cons,))
            a_col[i] = 1  

            c_grand_m = np.hstack([c_grand_m, M])  # COUT DE A = M
            A_grand_m = np.hstack([A_grand_m, a_col.reshape(-1, 1)])
            a_vars.append(len(c_grand_m) - 1)  
    
    afficher_premier_tableau(c_grand_m, A_grand_m, b)
    # UTILISATION DE LINPROG PUR OBTENIR LE RESULTAT DE LA SIMPLEXE
    result = linprog(c_grand_m, A_eq=A_grand_m, b_eq=b, method='simplex')

    print(result) #AFFICHER LE RESULTAT

    # RECUPERATION DE LA SOLUTION FINALE
    final_solution = result.x[:num_vars]
    return final_solution, result.fun

#TEST
if __name__ == "__main__":
   
   #LES COEFF DE LA FNCT OBJECTIF
    c = [-2, -3]  

    # LES COEFF DES CONTRAINTES
    A = np.array([
        [1, 2],    
        [2, 1]    
    ])
    b = np.array([8, 6])

    #LES SIGNES DES CONTRAINTES
    c_signe = ['<=', '>='] 

    # RESOLUTION
    solution, optimal_value = GrandM(c, A, b, c_signe)

    print("Solution optimale:")

    for i in range(len(solution)):
        
        print(f"x{i+1} = {solution[i]}")

    print("Valeur optimale de z:", -optimal_value)  # POUR LE PROBLEME DE MAX EN MULTIPLIE PAR -1
