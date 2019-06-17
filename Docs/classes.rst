=======
Classes
=======

.. module:: Vector

Classes
=======

.. class:: Vector2

    .. method:: __init__(x,y,override=False)

        :param int,float x:
            X position of Vector
        
        :param int,float y:
            Y position of Vector
        
        :param bool override:
            Used for Python's magic methods
        
    .. method:: add(vect)

        :param Vector2 vect:
            Vector2 to add to the current Vector
        
        Adds the X and Y coordinates to the current Vector2
    
    .. method:: subtract(vect)

        :param Vector2 vect:
            Vector2 to subtract to the current Vector
        
        Subtracts the X and Y coordinates to the current Vector2

    .. method:: multiply(vect)

        :param Vector2 vect:
            Vector2 to multiply to the current Vector
        
        Multiplies the X and Y coordinates to the current Vector2
    
    .. method:: multiply_scalar(scalar)

        :param int scalar:
            Multiplies the coordinates with a scalar number
    
    .. method:: normalize()

        Normalizes the Vector
    
    .. method:: dot(vect)

        :param Vector2 vect:
            Vector2 variable
        :return: Dot product of the Vectors
        :rtype: Vector2
    
    .. method:: magnitude()

        :return: Vector magnitude
        :rtype: int
    
    .. method:: copy()

        :return: Copy of the Vector object
        :rtype: Vector2
    
    .. method:: length()

        :return: Length of the Vector
        :rtype: float
    
    .. method:: length_squared()

        :return: Length squared of the Vector
        :rtype: int
    
    .. method:: rotate(angle)

        :param int angle:
            Angle, in degrees, to rotate the Vector

    .. method:: setMag(mag)

        :param int mag:
            Sets the Vector's new magnitude
        
    .. method:: fromAngle(angle)

        :param int,float angle:
            Angle for the Vector
        
        :return: Vector2 from angle
        :rtype: Vector2
        
        This is a static method, meaning it can be called without instanciating the Vector2 class
    
    .. method:: distance(vec1,vec2)

        :param Vector2 vec1:
        :param Vector2 vec2:
        :return: Distance between both Vectors
        :rtype: int

        This is a static method, meaning it can be called without instanciating the Vector2 class
    
