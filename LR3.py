import numpy as np
from typing import List, Dict

def create_pairwise_matrix(n: int, scale_values: List[List[int]]) -> np.ndarray:

    matrix = np.eye(n)
    
    idx = 0
    for i in range(n):
        for j in range(i+1, n):
            matrix[i][j] = scale_values[idx]
            matrix[j][i] = 1 / scale_values[idx]
            idx += 1
    
    return matrix


def normalize_matrix(matrix: np.ndarray) -> np.ndarray:

    col_sums = np.sum(matrix, axis=0)
    normalized = matrix / col_sums
    return normalized


def calculate_weights(matrix: np.ndarray) -> np.ndarray:
  
    normalized = normalize_matrix(matrix)
    weights = np.mean(normalized, axis=1)
    return weights


def consistency_check(matrix: np.ndarray, weights: np.ndarray) -> Dict[str, float]:

    n = len(matrix)
    

    Aw = matrix @ weights
    lambda_max = np.mean(Aw / weights)
    

    CI = (lambda_max - n) / (n - 1)
    

    RI_table = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 
                7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
    RI = RI_table.get(n, 1.49)
    

    CR = CI / RI if RI > 0 else 0
    
    return {
        'lambda_max': lambda_max,
        'CI': CI,
        'RI': RI,
        'CR': CR,
        'consistent': CR < 0.1
    }


def calculate_alternative_weights(criteria_weights: np.ndarray, 
                                   alternatives_matrices: List[np.ndarray]) -> np.ndarray:

    n_alternatives = len(alternatives_matrices[0])
    n_criteria = len(criteria_weights)
    

    alt_weights_matrix = np.zeros((n_alternatives, n_criteria))
    
    for i, matrix in enumerate(alternatives_matrices):
        alt_weights_matrix[:, i] = calculate_weights(matrix)
    

    final_weights = alt_weights_matrix @ criteria_weights
    
    return final_weights


def input_pairwise_matrix_data(n: int, element_names: List[str], comparison_type: str) -> List[int]:

    print(f"\n=== Сравнение {comparison_type} по шкале Саати ===")
    print("Шкала: 1=равно, 3=немного лучше, 5=лучше, 7=значительно лучше, 9=принципиально лучше")
    print("Промежуточные значения: 2, 4, 6, 8\n")
    
    values = []
    for i in range(n):
        for j in range(i+1, n):
            while True:
                try:
                    val = int(input(f"{element_names[i]} vs {element_names[j]} (1-9): "))
                    if 1 <= val <= 9:
                        values.append(val)
                        break
                    else:
                        print("Значение должно быть от 1 до 9!")
                except ValueError:
                    print("Введите целое число!")
    
    return values


def main():

    
    print("=" * 60)
    print("ВЫБОР УНИВЕРСИТЕТА МЕТОДОМ АНАЛИЗА ИЕРАРХИЙ (AHP)")
    print("=" * 60)
    

    while True:
        n_criteria = int(input("\nВведите количество критериев (минимум 5): "))
        if n_criteria >= 5:
            break
        print("Критериев должно быть не менее 5!")
    
    while True:
        n_alternatives = int(input("Введите количество альтернатив-университетов (минимум 3): "))
        if n_alternatives >= 3:
            break
        print("Альтернатив должно быть не менее 3!")
    
   
    print("\n--- Введите названия критериев ---")
    criteria_names = [input(f"Критерий {i+1}: ") for i in range(n_criteria)]
    
    print("\n--- Введите названия университетов ---")
    alternative_names = [input(f"Университет {i+1}: ") for i in range(n_alternatives)]
    
 
    print(f"\n{'='*60}")
    print("ШАГ 1: Сравнение критериев по важности для выбора университета")
    print(f"{'='*60}")
    
    criteria_scale_values = input_pairwise_matrix_data(
        n_criteria, criteria_names, "критериев"
    )
    
    criteria_matrix = create_pairwise_matrix(n_criteria, criteria_scale_values)
    criteria_weights = calculate_weights(criteria_matrix)
    criteria_consistency = consistency_check(criteria_matrix, criteria_weights)
    
    print(f"\n✓ Веса критериев:")
    for i, (name, weight) in enumerate(zip(criteria_names, criteria_weights)):
        print(f"  {name}: {weight:.4f} ({weight*100:.2f}%)")
    
    print(f"\n✓ Проверка согласованности: CR = {criteria_consistency['CR']:.4f}")
    if criteria_consistency['consistent']:
        print("  → Матрица согласована (CR < 0.1) ✓")
    else:
        print("  ⚠ Внимание: матрица может быть несогласована (CR >= 0.1)")
    

    print(f"\n{'='*60}")
    print("ШАГ 2: Сравнение университетов по каждому критерию")
    print(f"{'='*60}")
    
    alternatives_matrices = []
    
    for crit_idx, crit_name in enumerate(criteria_names):
        print(f"\n--- Критерий: {crit_name} ---")
        alt_scale_values = input_pairwise_matrix_data(
            n_alternatives, alternative_names, f"университетов по критерию '{crit_name}'"
        )
        
        alt_matrix = create_pairwise_matrix(n_alternatives, alt_scale_values)
        alternatives_matrices.append(alt_matrix)
        

        alt_weights = calculate_weights(alt_matrix)
        alt_consistency = consistency_check(alt_matrix, alt_weights)
        print(f"  CR = {alt_consistency['CR']:.4f} {'✓' if alt_consistency['consistent'] else '⚠'}")
    

    print(f"\n{'='*60}")
    print("РЕЗУЛЬТАТ: Итоговые приоритеты университетов")
    print(f"{'='*60}")
    
    final_weights = calculate_alternative_weights(criteria_weights, alternatives_matrices)
    

    sorted_indices = np.argsort(final_weights)[::-1]
    
    print(f"\n🏆 РЕЙТИНГ УНИВЕРСИТЕТОВ:")
    for rank, idx in enumerate(sorted_indices, 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else ""
        print(f"  {medal} {rank}. {alternative_names[idx]}: {final_weights[idx]:.4f} ({final_weights[idx]*100:.2f}%)")
    

    best_idx = sorted_indices[0]
    print(f"\n💡 РЕКОМЕНДАЦИЯ: Наиболее подходящий университет — {alternative_names[best_idx]}")
    
    return final_weights, sorted_indices


if __name__ == "__main__":
    main()