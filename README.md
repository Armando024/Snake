# Neural Network used to play classic Snake game

## Libraries:
    Please installed to compile, for instructions on how to install used the provided links.
    Numpy:
    https://www.scipy.org/scipylib/download.html
    TensorFlow:
    https://www.tensorflow.org/install/
    Pygame:
    https://www.pygame.org/wiki/GettingStarted
## To execute:
    In Mac OS/Linux, running the the instruction below in your terminal does the trick. 
        python3 main.py
## The data used to train the Neural Network:
    Inputs:
        Using the head of the snake as the main reference point to calculate if there were obstacles 
        in front of the snake or sides.
            If one was there there was an obstacle in front.
            If zero there was no obstacle.
            
        The orientation of the snake head to the apple like a compass.
            Calculated the angle between the snake and head
        
        |  a    -apple
        | /
        |/
        O   -head
        o   -body
        o
        o
        o

## Example gif
<img src="https://github.com/Armando024/old_aaguirre/blob/master/static/snake.gif" width="341.23" height="481.7"  />



    








