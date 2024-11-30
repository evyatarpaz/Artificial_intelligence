import ex1
import search
import time


def run_problem(func, targs=(), kwargs=None):
    if kwargs is None:
        kwargs = {}
    result = (-3, "default")
    try:
        result = func(*targs, **kwargs)

    except Exception as e:
        result = (-3, e)
    return result


# check_problem: problem, search_method, timeout
# timeout_exec: search_method, targs=[problem], timeout_duration=timeout
def solve_problems(problem, algorithm):
    for row in problem:
        print(row)

    try:
        p = ex1.create_zuma_problem(problem)
    except Exception as e:
        print("Error creating problem: ", e)
        return None
    if algorithm == "bfs":
        result = run_problem((lambda p: search.breadth_first_graph_search(p)), targs=[p])
    if algorithm == "gbfs":
        result = run_problem((lambda p: search.greedy_best_first_graph_search(p, p.h)),targs=[p])
    else:
        result = run_problem((lambda p: search.astar_search(p, p.h)), targs=[p])

    if result and isinstance(result[0], search.Node):
        solve = result[0].path()[::-1]
        solution = [pi.action for pi in solve][1:]
        print(len(solution), solution)
    else:
        print("no solution")


# problem1 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1), (1, 2, 3, 4, 1, 2, 3, 4))
# # solution1: len(solution) = 4
# problem2 = ((3, 3, 1, 4, 2, 4, 4, 1, 2, 4, 3), (2, 2, 2, 2, 4, 4, 1, 3))
# # solution2: len(solution) = 7

# problem3 = ((1, 1, 2, 2, 1, 1, 3, 3, 4, 4, 3, 1, 1),(2, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,3,3,3,3,1))
problem1 = ((1, 1), (1,))
problem2 = ((1, 2, 2, 1, 1), (2, 1))
problem3 = ((1, 2, 3, 3, 2, 2, 1, 1), (3,))
problem4 = ((2, 2, 3, 2), (3, 3))
problem5 = ((2, 2, 3, 2), (3, 3, 2, 1, 2, 2, 4))
problem6 = ((2, 2, 3, 3, 2), (1, 3))
problem7 = ((3, 3, 4, 4, 3, 3), (3, 4))
problem8 = ((1, 1, 2, 2, 1, 1, 3, 3, 4, 4, 3, 1, 1), (2, 4, 3, 3, 3, 1))
problem9 = ((2, 3, 3, 2), (1, 2, 3))
problem10 = ((4, 1, 2, 3, 3, 2, 2, 1, 1), (4, 3, 4))
problem11 = ((1, 1, 3, 3, 2, 2, 3, 3, 2, 2, 3, 3, 2, 4, 1, 1, 4, 3, 3, 2, 2, 3, 3, 1, 1), (3, 4, 1, 2, 3, 4))
problem12 = ((2, 2, 3, 3, 1), (1, 1, 2, 3))
problem13 = ((4, 2, 2, 3, 3, 2), (1, 3, 4, 4))
problem14 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1), (1, 2, 3, 4))
problem15 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1), (1, 2, 3, 4, 1, 2, 3, 4))
problem16 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1, 2, 2), (1, 2, 3, 4, 1, 2))
problem17 = ((1, 1, 3, 3, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 3, 3, 1, 1), (1, 2, 3, 4, 1, 2, 3, 4))
problem18 = ((2, 2, 3, 3, 1), (4, 1, 1, 2, 3))
problem19 = ((1, 2, 2, 1, 1, 3, 3, 1), (4, 2, 3, 4, 4, 3, 2, 3, 2, 2, 3, 1, 1))
problem20 = ((1, 1, 2, 4, 1, 1, 4, 3, 3, 2, 2, 3, 3, 1, 1), (3, 4, 1, 2, 3, 4))
problem21 = ((1, 1, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1, 2, 2), (1, 2, 3, 4, 2, 3, 4))
problem22 = ((1, 1, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1, 2, 2), (1, 2, 3, 4, 1, 3))
problem23 = ((3, 3, 4, 4, 3, 3), (3, 1, 2, 3, 2, 1, 4))
problem24 = ((1, 3, 3, 2, 1, 2, 2), (1, 3, 2, 4, 2, 3, 2))
problem25 = ((3, 3, 1, 4, 2, 4, 4, 1, 2, 4, 3), (2, 2, 2, 2, 4, 4, 1, 3))
problem26 = ((1, 3, 3, 2, 1, 2, 2), (1, 3, 2, 4, 2, 3, 4, 2))
problem27 = ((1, 2, 1, 2), (1, 2, 4, 1, 2, 2, 4, 1, 3, 2, 1, 2))
problem28 = ((2, 2, 3, 2), (3, 1))
problem29 = ((4, 2, 2, 3, 3, 2), (1, 3))
problem30 = ((2, 2, 3, 3, 2, 4), (2, 2, 3, 2))
problem31 = ((4, 2, 2, 3, 3, 2), (1, 3, 4))
problem32 = ((4, 2, 2, 3, 3, 1), (1, 1, 2, 3))
problem33 = ((1, 2, 2, 1, 1, 3, 3, 1), (4, 2, 3, 4, 4, 2, 1))
problem34 = ((1, 1, 3, 3, 2, 2, 3, 1, 2, 3, 3, 2, 2, 3, 3, 1, 1), (3, 1, 2, 4, 3, 4, 3, 1))
problem35 = ((1, 1, 3, 3, 2, 2, 3, 1, 4, 2, 3, 3, 2, 2, 3, 3, 1, 1), (3, 4, 1, 2, 4, 3, 4, 3, 1))
problem36 = ((1, 1, 2, 2, 1, 1, 3, 3, 4, 4, 3, 1, 1), (3, 3, 3, 3, 3, 2, 4, 3, 3, 3, 1))
problem37 = ((3, 3, 1, 1, 4, 3, 2, 4, 3, 3, 2, 4, 4, 1, 3), (4, 4, 2, 2, 3, 3, 3, 1, 3))
def main():
    
    algorithm = ["gbfs","astar"]  # or "astar"
    problem = [problem1, problem2, problem3, problem4, problem5, problem6, problem7, problem8, problem9, problem10, problem11, problem12, problem13, problem14, problem15, problem16, problem17, problem18, problem19, problem20, problem21, problem22, problem23, problem24, problem25, problem26, problem27, problem28, problem29, problem30, problem31, problem32, problem33, problem34, problem35, problem36, problem37]
    i = 1
    for p in problem:
        for a in algorithm:
            print(f"Problem:{i}")
            print("Algorithm: ", a)
            start_time = time.time()
            solve_problems(p, a)
            end_time = time.time()
            print("Time: ", end_time - start_time)
            print("")
        i += 1

if __name__ == '__main__':
    main()
