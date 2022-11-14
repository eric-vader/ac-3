import queue

class CSPSolver:
    worklist = queue.Queue()  # a queue of arcs (this can be a queue or set in ac-3)

    # arcs: list of tuples
    # domains: dict of { tuples: list }
    # constraints: dict of { tuples: list }
    def __init__(self, arcs: list, domains: dict, constraints: dict):
        self.arcs = arcs
        self.domains = domains
        self.constraints = constraints

    # returns an empty dict if an inconsistency is found and domains for variables otherwise
    # generate: bool (choose whether or not to use a generator)
    def solve(self, generate=False) -> dict:
        result = self.solve_helper()

        if generate:
            return result
        else:
            return_value = []

            for step in result:
                if step == None:
                    return step  # inconsistency found
                else:
                    return_value = step

            return return_value[1]  # return only the final domain

    # returns a generator for each step in the algorithm, including the end result
    # each yield is a tuple containing: (edge, new domains, edges to consider)
    def solve_helper(self) -> dict:
        # setup queue with given arcs
        [self.worklist.put(arc) for arc in self.arcs]

        # continue working while worklist is not empty
        while not self.worklist.empty():
            (xi, xj) = self.worklist.get()

            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    # found an inconsistency
                    yield None
                    break

                # get all of xj's neighbors
                neighbors = [neighbor for neighbor in self.arcs if neighbor[0] == xj]
                
                # put all neighbors into the worklist to be evaluated
                [self.worklist.put(neighbor) for neighbor in neighbors]

                yield ((xi, xj), self.domains, neighbors)
            else:
                yield ((xi, xj), self.domains, None)

        # yield the final return value
        yield (None, self.domains, None)

    # returns true if and only if the given domain i
    def revise(self, xi: object, xj: object) -> bool:
        revised = False

        # get the domains for xi and xj
        xi_domain = self.domains[xi]
        xj_domain = self.domains[xj]

        # get a list of constraints for (xi, xj)
        constraints = [constraint for constraint in self.constraints if constraint[0] == xi and constraint[1] == xj]

        for x in xi_domain[:]:
            satisfies = False  # there is a value in xjDomain that satisfies the constraint(s) between xi and xj

            for y in xj_domain:
                for constraint in constraints:
                    check_function = self.constraints[constraint]

                    # check y against x for each constraint
                    if check_function(x, y):
                        satisfies = True

            if not satisfies:
                # delete x from xiDomain
                xi_domain.remove(x)
                revised = True

        return revised


# from sortedcontainers import SortedSet
# from operator import eq, neg

# def dom_j_up(csp, queue):
#     return SortedSet(queue, key=lambda t: neg(len(csp.curr_domains[t[1]])))

# def revise(csp, Xi, Xj, removals, checks=0):
#     """Return true if we remove a value."""
#     revised = False
#     for x in csp.curr_domains[Xi][:]:
#         # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
#         # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
#         conflict = True
#         for y in csp.curr_domains[Xj]:
#             if csp.constraints(Xi, x, Xj, y):
#                 conflict = False
#             checks += 1
#             if not conflict:
#                 break
#         if conflict:
#             csp.prune(Xi, x, removals)
#             revised = True
#     return revised, 

# def AC3(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
#     """[Figure 6.3]"""
#     if queue is None:
#         queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
#     csp.support_pruning()
#     queue = arc_heuristic(csp, queue)
#     checks = 0
#     while queue:
#         (Xi, Xj) = queue.pop()
#         revised, checks = revise(csp, Xi, Xj, removals, checks)
#         if revised:
#             if not csp.curr_domains[Xi]:
#                 return False, checks  # CSP is inconsistent
#             for Xk in csp.neighbors[Xi]:
#                 if Xk != Xj:
#                     queue.add((Xk, Xi))
#     return True, checks  # CSP is satisfiable