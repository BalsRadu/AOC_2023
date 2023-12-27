"""
--- Day 24: Never Tell Me The Odds ---
It seems like something is going wrong with the snow-making process. Instead of forming snow, the water that's been absorbed into the air seems to be forming hail!

Maybe there's something you can do to break up the hailstones?

Due to strong, probably-magical winds, the hailstones are all flying through the air in perfectly linear trajectories. You make a note of each hailstone's position and velocity (your puzzle input). For example:

19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
Each line of text corresponds to the position and velocity of a single hailstone. The positions indicate where the hailstones are right now (at time 0). The velocities are constant and indicate exactly how far each hailstone will move in one nanosecond.

Each line of text uses the format px py pz @ vx vy vz. For instance, the hailstone specified by 20, 19, 15 @ 1, -5, -3 has initial X position 20, Y position 19, Z position 15, X velocity 1, Y velocity -5, and Z velocity -3. After one nanosecond, the hailstone would be at 21, 14, 12.

Perhaps you won't have to do anything. How likely are the hailstones to collide with each other and smash into tiny ice crystals?

To estimate this, consider only the X and Y axes; ignore the Z axis. Looking forward in time, how many of the hailstones' paths will intersect within a test area? (The hailstones themselves don't have to collide, just test for intersections between the paths they will trace.)

In this example, look for intersections that happen with an X and Y position each at least 7 and at most 27; in your actual data, you'll need to check a much larger test area. Comparing all pairs of hailstones' future paths produces the following results:

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 18, 19, 22 @ -1, -1, -2
Hailstones' paths will cross inside the test area (at x=14.333, y=15.333).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 20, 25, 34 @ -2, -2, -4
Hailstones' paths will cross inside the test area (at x=11.667, y=16.667).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=6.2, y=19.4).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for hailstone A.

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 20, 25, 34 @ -2, -2, -4
Hailstones' paths are parallel; they never intersect.

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=-6, y=-5).

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for both hailstones.

Hailstone A: 20, 25, 34 @ -2, -2, -4
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=-2, y=3).

Hailstone A: 20, 25, 34 @ -2, -2, -4
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for hailstone B.

Hailstone A: 12, 31, 28 @ -1, -2, -1
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for both hailstones.
So, in this example, 2 hailstones' future paths cross inside the boundaries of the test area.

However, you'll need to search a much larger test area if you want to see if any hailstones might collide. Look for intersections that happen with an X and Y position each at least 200000000000000 and at most 400000000000000. Disregard the Z axis entirely.

Considering only the X and Y axes, check all pairs of hailstones' future paths for intersections. How many of these intersections occur within the test area?

Your puzzle answer was 31921.

--- Part Two ---
Upon further analysis, it doesn't seem like any hailstones will naturally collide. It's up to you to fix that!

You find a rock on the ground nearby. While it seems extremely unlikely, if you throw it just right, you should be able to hit every hailstone in a single throw!

You can use the probably-magical winds to reach any integer position you like and to propel the rock at any integer velocity. Now including the Z axis in your calculations, if you throw the rock at time 0, where do you need to be so that the rock perfectly collides with every hailstone? Due to probably-magical inertia, the rock won't slow down or change direction when it collides with a hailstone.

In the example above, you can achieve this by moving to position 24, 13, 10 and throwing the rock at velocity -3, 1, 2. If you do this, you will hit every hailstone as follows:

Hailstone: 19, 13, 30 @ -2, 1, -2
Collision time: 5
Collision position: 9, 18, 20

Hailstone: 18, 19, 22 @ -1, -1, -2
Collision time: 3
Collision position: 15, 16, 16

Hailstone: 20, 25, 34 @ -2, -2, -4
Collision time: 4
Collision position: 12, 17, 18

Hailstone: 12, 31, 28 @ -1, -2, -1
Collision time: 6
Collision position: 6, 19, 22

Hailstone: 20, 19, 15 @ 1, -5, -3
Collision time: 1
Collision position: 21, 14, 12
Above, each hailstone is identified by its initial position and its velocity. Then, the time and position of that hailstone's collision with your rock are given.

After 1 nanosecond, the rock has exactly the same position as one of the hailstones, obliterating it into ice dust! Another hailstone is smashed to bits two nanoseconds after that. After a total of 6 nanoseconds, all of the hailstones have been destroyed.

So, at time 0, the rock needs to be at X position 24, Y position 13, and Z position 10. Adding these three coordinates together produces 47. (Don't add any coordinates from the rock's velocity.)

Determine the exact position and velocity the rock needs to have at time 0 so that it perfectly collides with every hailstone. What do you get if you add up the X, Y, and Z coordinates of that initial position?

Your puzzle answer was 761691907059631.
"""
from itertools import combinations
from sympy import symbols, Eq, solve

def read_hailstones_data(lines):
    hailstones = []
    for line in lines:
        parts = line.strip().split('@')
        position = tuple(map(int, parts[0].strip().split(',')))
        velocity = tuple(map(int, parts[1].strip().split(',')))
        hailstones.append((position, velocity))
    return hailstones


def find_intersection(hailstone1, hailstone2):
    """
    Finds the intersection point of two hailstones' paths, if it exists.
    Each hailstone is represented as (position, velocity) where position and velocity are tuples.
    """
    pos1, vel1 = hailstone1
    pos2, vel2 = hailstone2

    # Check for parallel lines (no intersection)
    if vel1[0] * vel2[1] == vel1[1] * vel2[0]:
        return None

    # Solving the linear equations to find the intersection
    denominator = vel1[0] * vel2[1] - vel1[1] * vel2[0]
    t = (pos2[0] * vel2[1] - pos2[1] * vel2[0] - pos1[0] * vel2[1] + pos1[1] * vel2[0]) / denominator
    # Check if intersection occurs in the future for both hailstones
    if t < 0:
        return None

    # Calculate the intersection point
    intersection_x = pos1[0] + t * vel1[0]
    intersection_y = pos1[1] + t * vel1[1]
    # Check if the intersection occurs in the future for both hailstones
    # Considering the case where the hailstone might have crossed the intersection point in the past
    future_for_h1 = (intersection_x - pos1[0]) / vel1[0] >= 0 if vel1[0] != 0 else True
    future_for_h2 = (intersection_x - pos2[0]) / vel2[0] >= 0 if vel2[0] != 0 else True
    if not (future_for_h1 and future_for_h2):
        return None

    return intersection_x, intersection_y

def count_intersections(hailstones, min_x, max_x, min_y, max_y):
    """
    Counts the number of intersections within the specified test area.
    """
    count = 0
    for h1, h2 in combinations(hailstones, 2):
        intersection = find_intersection(h1, h2)
        if intersection:
            x, y = intersection
            if min_x <= x <= max_x and min_y <= y <= max_y:
                count += 1
    return count


def find_rock_trajectory(hailstones):
    """
    Finds the rock's trajectory that intersects with all given hailstones.
    The trajectory is determined by solving a system of equations derived from
    the condition that the rock's path intersects with each hailstone's path at some point.

    Mathematical Derivation:
    1. Each hailstone's path is defined by its initial position (x_i, y_i, z_i)
       and velocity (v_ix, v_iy, v_iz). The position at any time t is given by:
       r_hailstone = (x_i, y_i, z_i) + t * (v_ix, v_iy, v_iz).
    2. The rock's path is defined by its unknown initial position (x0, y0, z0)
       and velocity (v0x, v0y, v0z). The position at time t is:
       r_rock = (x0, y0, z0) + t * (v0x, v0y, v0z).
    3. For the rock to intersect with a hailstone's path, their positions must be equal at
       some time t, leading to three equations per hailstone.
    4. By rearranging and setting terms involving t equal, we eliminate t and simplify
       the equations to two per hailstone:
       (x0 - xi) / (vix - v0x) = (y0 - yi) / (viy - v0y)
       (y0 - yi) / (viy - v0y) = (z0 - zi) / (viz - v0z)
    5. For N hailstones, this process results in 2N equations. The system of equations
       is then solved to find the rock's initial position and velocity.

    The function generates these equations for each hailstone and solves the resulting system.
    If an integer solution exists, it is returned; otherwise, the function returns None.

    """
    # Define symbols
    x0, y0, z0, v0x, v0y, v0z = symbols('x0 y0 z0 v0x v0y v0z')
    x_i, y_i, z_i, v_ix, v_iy, v_iz = symbols('x_i y_i z_i v_ix v_iy v_iz')

    # Equation templates
    eq1_template = Eq((x0 - x_i) * (v0y - v_iy) - (y0 - y_i) * (v0x - v_ix), 0)
    eq2_template = Eq((y0 - y_i) * (v0z - v_iz) - (z0 - z_i) * (v0y - v_iy), 0)

    # Generate equations for the hailstones
    equations = []
    for hailstone in hailstones:
        pos, vel = hailstone
        equations.append(eq1_template.subs({x_i: pos[0], y_i: pos[1], z_i: pos[2], v_ix: vel[0], v_iy: vel[1], v_iz: vel[2]}))
        equations.append(eq2_template.subs({x_i: pos[0], y_i: pos[1], z_i: pos[2], v_ix: vel[0], v_iy: vel[1], v_iz: vel[2]}))

    # Solve the system of equations
    solution = solve(equations, (x0, y0, z0, v0x, v0y, v0z))

    # Verify if the solution consists of integer values
    for sol in solution:
        if all(s.is_Integer for s in sol):
            return sum(sol[0:3])

    return None

with open('input.txt', 'r') as file:
    hailstones = read_hailstones_data(file.readlines())
    # Defining the test area boundaries
    min_x, max_x = 200000000000000, 400000000000000
    min_y, max_y = 200000000000000, 400000000000000

    # Counting the intersections
    intersection_count = count_intersections(hailstones, min_x, max_x, min_y, max_y)

    # Finding the rock's trajectory
    rock_trajectory = find_rock_trajectory(hailstones[:3])

    print("First puzzle solution:", intersection_count)
    print("Second puzzle solution:", rock_trajectory)