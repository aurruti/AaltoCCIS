import numpy as np
from matplotlib import pyplot as plt

def max_button_size(p, A, s_min, max_iter=10, show_progress=True):
    n = len(p)

    # Initialization
    sizes = np.ones(n) * s_min
    if np.sum(sizes) >= A:
        raise ValueError("The minimum size of each button is too large, or there are too many buttons.")
    
    remaining_space = A - np.sum(sizes)

    # Calculate the initial delta increase (if the max iterations are set to less than 1, the initial allocation is returned)
    if max_iter > 0:
        delta_increase = remaining_space / n
    else:
        return sizes

    iteration = 0

    while remaining_space > 0 and iteration < max_iter:
        if show_progress:
            print(f"Iteration {iteration + 1}: Allocated {A - remaining_space:.2f} out of {A} area units.", end='\r')

        random_indices = np.random.permutation(n)
        # Assign new space to the buttons, according to their priority values
        for i in random_indices:
            # The size delta increase of each button is proportional to its priority value
            i_increase = delta_increase * p[i]
            if i_increase <= remaining_space:
                sizes[i] += i_increase
                remaining_space -= i_increase

            # Unless the button increase would exceed the available space
            else:
                break
        
        # Delta increase decay
        delta_increase *= 0.5 # Decay
        iteration += 1

    if show_progress:
        print("\nOptimization Complete!")
        print("")
        print("For buttons with priorities:")
        print(p)
        print("The found optimal sizes are:")
        print(sizes)
        print(f"Total space used: {A - remaining_space:.2f} out of {A} area units.")
        print("")
    
    return sizes, sum(sizes)
        
def plot_iteration_improvent(p, A, s_min, iterations):
    spaces = []
    for i in iterations:
        _, space_used = max_button_size(p, A, s_min, i, False)
        spaces.append(space_used)

    plt.plot(iterations, spaces)


if __name__ == "__main__":
    # Variable definitions
    p = np.array([0.2, 0.3, 0.5, 1])
    p_2 = np.array([0.4, 0.7, 0.8, 1, 0.5])   # Button priority (0-1)
    p_5 = np.random.rand(10)                  # Button priority (0-1)        
    p_3 = np.random.rand(10**3)               # Button priority (0-1)
    p_4 = np.random.rand(10**4)               # Button priority (0-1)
    A = 10**6                                 # Available screen area
    s_min = 20                                # Minimum size for each button
    
    # Function call
    sizes, _ = max_button_size(p, 1000, s_min)
    sizes_2, _ = max_button_size(p_2, 1000, s_min)
    sizes_5, _ = max_button_size(p_5, 1000, s_min, show_progress=False)
    print("Total space used for 10 buttons:", sum(sizes_5))
    sizes_3, allocated_3 = max_button_size(p_3, A, s_min, show_progress=False)
    print("Total space used for 1000 buttons:", allocated_3)
    sizes_4, allocated_4 = max_button_size(p_4, A, s_min, show_progress=False)
    print("Total space used for 10000 buttons:", allocated_4)

    # Plotting improvement with iterations
    iterations = range(2, 15)
    plt.figure()
    plot_iteration_improvent(p, A, s_min, iterations)
    plot_iteration_improvent(p_2, A, s_min, iterations)
    plot_iteration_improvent(p_5, A, s_min, iterations)
    plot_iteration_improvent(p_3, A, s_min, iterations)
    plot_iteration_improvent(p_4, A, s_min, iterations)
    plt.plot(iterations, [A] * len(iterations), linestyle='--', color='black')
    plt.legend(["p = [0.2, 0.3, 0.5, 1]", "p = [0.4, 0.7, 0.8, 1, 0.5]", "Random p (10 buttons)", "Random p (10^3 buttons)", "Random p (10^4 buttons)", "Available Space"])
    plt.xlabel("Iterations")
    plt.ylabel("Allocated Space")
    plt.yscale("log")
    # plt.xscale("log")
    plt.title("Button Size Optimization")
    plt.show()

    # three more toy examples
    p_toy_1 = np.random.rand(5).round(1)
    p_toy_2 = np.random.rand(5).round(1)
    p_toy_3 = np.random.rand(5).round(1)
    sizes_toy_1, at1 = max_button_size(p_toy_1, 1000, s_min, show_progress=False)
    sizes_toy_2, at2 = max_button_size(p_toy_2, 1000, s_min, show_progress=False)
    sizes_toy_3, at3 = max_button_size(p_toy_3, 1000, s_min, show_progress=False)

    print(p_toy_1)
    print(sizes_toy_1.round(1))
    print(at1.round(1))
    print(p_toy_2)
    print(sizes_toy_2.round(1))
    print(at2.round(1))
    print(p_toy_3)
    print(sizes_toy_3.round(1))
    print(at3.round(1))