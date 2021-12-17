# gantryDeckLeveling
Deck leveling for gantry systems using fiducial points and a probe


# Key: 
* P0 – first point
* P1 – second point
* P2 – third point
* Pθ - pitch angle of rotation
* Rθ – roll angle of rotation
* Yθ – yaw angle of rotation
* xDiff - difference in x coordinates
* yDiff - difference in y coordinates
* NP - updated (new) point while transforming a point
* W – largest radius of probe/sensors

<p align="center">
  <img src="https://user-images.githubusercontent.com/71296226/146598093-b69f6de4-5857-46fe-87b8-1941f416c2d3.jpg" alt="alt text" width="500" height="700">
</p>


# Probing:
* Place the probe on the end effector flat into the center of the three fiducial points and press any key
* They are located at the corners of the deck
* Start at P0 in the bottom left and move counterclockwise sequentially to P2
* The points form the vertices of a right angle, P1 having a straight line to both P2 and P0
* Aquire the coordinate three points (x, y, z) from the liquid handler software
  
![image](https://user-images.githubusercontent.com/71296226/146596780-42aeec99-3bf5-44de-ba5f-05b4d44c3a6c.png)


# Calculate Yaw:
	Find the difference in the x and y coordinates of P1 and P2 from P1[y] == P2[y]
	The angle of rotation of the deck is arctan⁡(yDiff/xDiff), with the initial zero being the vertical x-axis*
  
  ![image](https://user-images.githubusercontent.com/71296226/146596744-3296189a-4b96-4a61-a9ee-6c5e9a4af9b1.png)


# Calculate Pitch:
	Find the difference in the y and z coordinates of P0 and P1 from P0[z] == P1[z] 
	The angle of rotation of the deck is arctan⁡(zDiff/yDiff)*
  
  ![image](https://user-images.githubusercontent.com/71296226/146596730-0c22b205-e731-4f27-a311-8803a82c643c.png)


# Calculate Roll:
	Find the difference in the x and z coordinates of P2 and P1 from P2[z] == P1[z]
	The angle of rotation of the deck is arctan⁡(zDiff/xDiff)*
  
  ![image](https://user-images.githubusercontent.com/71296226/146596719-a2b90c1a-e2fc-4682-84d6-3efa001e1154.png)

* Checks if this angle in degrees is exactly 90, 180, or 270 degrees first (to avoid errors/incorrect math)


# Point Transformations:
The point (x, y, z) is passed in which is transformed to a new point, NP, with coordinates (x’, y’, x’)

	Pitch (Pθ):
	x'=x
	y^'=(y+P1[y])*cos⁡(Pθ)-(z-P1[z])*sin⁡(Pθ)-P1[y]
	z^'=(z-P1[z])*cos⁡(Pθ)+(y+P1[y])*sin⁡(Pθ)+P1[z]
  
	Roll (Rθ):
	x^'=NP[x]+ (x+P1[x])*cos⁡(Rθ)+(z-P1[z])*sin⁡(Rθ)-P1[x]
	y'=y
	z^'=NP[z]+ (z-P1[z])*cos⁡(Rθ)-(x+P1[x])*sin⁡(Rθ)+P1[z]
  
	Yaw (Yθ):
	x^'=NP[x]+ x*cos⁡(Yθ)-y*sin⁡(Yθ)
	y=NP[y]+ y*cos⁡(Yθ)+x*sin⁡(Yθ)
	z'=z
  
	The radius (W) of the probe/sensor on the end effector can also be accounted for:
	z’ = NP[z] + (W * sin(Pθ) / sin(90) – Pθ)
  
  ![image](https://user-images.githubusercontent.com/71296226/146596695-da76d6b0-255c-4133-867e-ab4adf87687d.png)

