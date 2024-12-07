import pygame

# no penalty rewards
def barebones_reward_structure(snake, food):
    if snake.positions[0] == food.position:
        snake.length += 1
        food.reset()
    food.update()
    
# snake gains 1 length if fresh, and loses 1 length if decayed
def default_reward_structure(snake, food, grid_size, width, height):
    snake_head = snake.positions[0]
    head_x, head_y = snake_head

    # penalize proximity to walls
    wall_penalty = 0
    if head_x < 2 * grid_size or head_x > width - 2 * grid_size:
        wall_penalty -= 0.5
    if head_y < 2 * grid_size or head_y > height - 2 * grid_size:
        wall_penalty -= 0.5

    # reward for eating food
    if snake.positions[0] == food.position:
        if food.decayed:
            snake.length -= 1
            food.reset()
            return -5 + wall_penalty
        else:
            snake.length += 1
            food.reset()
            return 10 + wall_penalty

    food.update()
    return -0.1 + wall_penalty


# penalty for rotten food increases as time passes
def time_sensitive_rewards(snake, food, number_of_penalties=3, penalty_rate=5000):
    current_time = pygame.time.get_ticks()
    time_passed = current_time - food.spawn_time
    
    if(time_passed >= penalty_rate * (food.penalty + 2)):
        food.penalty += 1
            
    if snake.positions[0] == food.position:
        if food.decayed:
            snake.length -= 1 + food.penalty
            for i in range (1 + food.penalty):               
                if(len(snake.positions) > snake.length):
                    snake.positions.pop()
        else:   
            snake.length += 1
        food.reset()

    # respawn the food after increasing the penalty for rotten food a certain number of times
    food.update((penalty_rate * number_of_penalties * 10000))

# snake gains a multiplier for every n consecutively eaten fruit
def multiplier_reward_structure(snake, food, n=5):
    if snake.positions[0] == food.position:
        if food.decayed:
            snake.length -= 1
            if(len(snake.positions) > snake.length):
                snake.positions.pop()
            snake.multiplier = 1
            snake.fresh_fruit_combo = 0
        else: 
            snake.fresh_fruit_combo += 1
            
            if snake.fresh_fruit_combo > n:
                snake.multiplier += 1 
                snake.fresh_fruit_combo = 0 
                
            snake.length += snake.multiplier
            
        food.reset()
        
    food.update()
        
# snake gains a bonus for reaching milestones
def milestone_reward_structure(snake, food):
    if snake.positions[0] == food.position:
        if food.decayed:
            snake.length -= 1
            if(len(snake.positions) > snake.length):
                snake.positions.pop()
        else:
            snake.length += 1
            
            # milestones
            if snake.length == 10:
                snake.length += 2
            elif snake.length == 30:
                snake.length += 5
            elif snake.length == 100:
                snake.length += 10
                
        food.reset()
        
    food.update()
