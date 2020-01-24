Explanation of custom module and relative layout use in code

Components:
	Components are frames that can contain other components and drawables such as buttons.
	Components allow for the positioning of objects about the screen.

Relative Layout:
	A relative layout allows objects to be placed and sized relative to other objects.
	Ex: Making an objects match the screen dimentions.
	Ex2: Making and object stay in bottom left corner of another object regardless of movement and screen resizing


.set_relative(parent)
	- Sets the layout of the object as relative (explained above) rather than fixed layout (defined by coordinates)

.layout.w = frame.MATCH
	- Sets width of object equal to the width of the component that it is contained in

.layout.h = frame.MATCH
	- Sets height of object equal to the height of the component that it is contained in

.margin_*side* = int
	- Adds blank pixels on the specified side of the object

.gravity = "left right bottom top centerx centery"
	- Places object to specified side of the component that contains it
	- Ex: "right centery" will place the object to the right of the component and center it on the y axis

.align_*side* = index
	- Aligns the specified side of the object to the corresponding side of the object, specified by the index, in the same component
	- Ex: .align_left = 2 will align the left side of the object to the right side of the another object (object at index 2)