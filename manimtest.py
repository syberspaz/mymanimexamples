import numpy as np
from manimlib import *

class AnimatingMethods(Scene):
    def construct(self):
        grid = Tex(R"\pi").get_grid(10, 10, height=4)
        self.add(grid)

        # You can animate the application of mobject methods with the
        # ".animate" syntax:
        self.play(grid.animate.shift(LEFT))

        # Both of those will interpolate between the mobject's initial
        # state and whatever happens when you apply that method.
        # For this example, calling grid.shift(LEFT) would shift the
        # grid one unit to the left, but both of the previous calls to
        # "self.play" animate that motion.

        # The same applies for any method, including those setting colors.
        self.play(grid.animate.set_color(YELLOW))
        self.wait()
        self.play(grid.animate.set_submobject_colors_by_gradient(BLUE, GREEN))
        self.wait()
        self.play(grid.animate.set_height(TAU - MED_SMALL_BUFF))
        self.wait()

        # The method Mobject.apply_complex_function lets you apply arbitrary
        # complex functions, treating the points defining the mobject as
        # complex numbers.
        self.play(grid.animate.apply_complex_function(np.exp), run_time=5)
        self.wait()

        # Even more generally, you could apply Mobject.apply_function,
        # which takes in functions form R^3 to R^3
        self.play(
            grid.animate.apply_function(
                lambda p: [
                    p[0] + 0.5 * math.sin(p[1]),
                    p[1] + 0.5 * math.sin(p[0]),
                    p[2]
                ]
            ),
            run_time=5,
        )
        self.wait()



class TexTransformExample(Scene):
    def construct(self):
        # Tex to color map
        t2c = {
            "A": BLUE,
            "B": TEAL,
            "C": GREEN,
        }
        # Configuration to pass along to each Tex mobject
        kw = dict(font_size=72, t2c=t2c)
        lines = VGroup(
            Tex("A^2 + B^2 = C^2", **kw),
            Tex("A^2 = C^2 - B^2", **kw),
            Tex("A^2 = (C + B)(C - B)", **kw),
            Tex(R"A = \sqrt{(C + B)(C - B)}", **kw),
        )
        lines.arrange(DOWN, buff=LARGE_BUFF)

        self.add(lines[0])
        # The animation TransformMatchingStrings will line up parts
        # of the source and target which have matching substring strings.
        # Here, giving it a little path_arc makes each part rotate into
        # their final positions, which feels appropriate for the idea of
        # rearranging an equation
        self.play(
            TransformMatchingStrings(
                lines[0].copy(), lines[1],
                # matched_keys specifies which substring should
                # line up. If it's not specified, the animation
                # will align the longest matching substrings.
                # In this case, the substring "^2 = C^2" would
                # trip it up
                matched_keys=["A^2", "B^2", "C^2"],
                # When you want a substring from the source
                # to go to a non-equal substring from the target,
                # use the key map.
                key_map={"+": "-"},
                path_arc=90 * DEGREES,
            ),
        )
        self.wait()
        self.play(TransformMatchingStrings(
            lines[1].copy(), lines[2],
            matched_keys=["A^2"]
        ))
        self.wait()
        self.play(
            TransformMatchingStrings(
                lines[2].copy(), lines[3],
                key_map={"2": R"\sqrt"},
                path_arc=-30 * DEGREES,
            ),
        )
        self.wait(2)
        self.play(LaggedStartMap(FadeOut, lines, shift=2 * RIGHT))

        # TransformMatchingShapes will try to line up all pieces of a
        # source mobject with those of a target, regardless of the
        # what Mobject type they are.
        source = Text("the morse code", height=1)
        target = Text("here come dots", height=1)
        saved_source = source.copy()

        self.play(Write(source))
        self.wait()
        kw = dict(run_time=3, path_arc=PI / 2)
        self.play(TransformMatchingShapes(source, target, **kw))
        self.wait()
        self.play(TransformMatchingShapes(target, saved_source, **kw))
        self.wait()


class GridExample(Scene):
    def construct(self):
        grid = NumberPlane((-5, 5), (-5, 5))
        
        axes = Axes(
            # x-axis ranges from -1 to 10, with a default step size of 1
            x_range=(-5, 5,1),
            # y-axis ranges from -2 to 2 with a step size of 0.5
            y_range=(-5, 5, 1),
            # The axes will be stretched so as to match the specified
            # height and width
            
            # Axes is made of two NumberLine mobjects.  You can specify
            # their configuration with axis_config
            axis_config=dict(
                stroke_color=GREY_A,
                stroke_width=2,
                numbers_to_exclude=[0],
            ),
            # Alternatively, you can specify configuration for just one
            # of them, like this.
            y_axis_config=dict(
                big_tick_numbers=[-2, 2],
            )
        )
        
        
        axes.add_coordinate_labels(
            font_size=20,
            num_decimal_places=1,
        )
   
       # t1 = ValueTracker(10)
       # number = always_redraw(lambda: DecimalNumber(t1.get_value(), num_decimal_places = 0))
       # self.play(Write(number))
       # self.play(t1.animate.set_value(30))
       # self.wait()
        
        self.play(
            ShowCreation(grid),
        )
        self.play(ShowCreation(axes))
        
        # trace out images
        mario = ImageMobject("images/Mario-Sprite.png")
        vec_a = np.array([0, 0, 0])
        dot1 = Dot(point=LEFT, radius=0.25,color=RED).move_to(vec_a)
        square_m = Square(side_length=mario.height, color=RED).move_to(vec_a)
        
        self.play(FadeIn(mario, scale=0.5))
        self.wait()
        self.play(ShowCreation(square_m))
        self.wait()

        self.play(FadeIn(dot1))
        self.wait()
        vt = ValueTracker(100)

        #mario.add_updater(lambda m: m.fade(darkness=vt.get_value()/100.0))
        #self.play(vt.animate.set_value(10),vt2, run_time=2, rate_func=linear)
        #vt.add_updater(lambda mobject: mobject.set_value(vt.get_value()-1))
        #self.wait(0.5)
        self.wait()

# a sprite containing an image, position vector, dot, etc .... 
class Sprite(Group):
    def __init__(self,
            image_dir="images/",
            image_file="Mario-Sprite.png",
            position = np.array([0,0,0]),
            dot_radius=0.25,
            dot_color=GREEN,
            dot_point=LEFT,
            square_color=RED,
            square_show=False,
            dot_show=True,
            coordsys=[],
            image_height=2,
            **kwargs):
        super().__init__(**kwargs)
        self.position_history=[]
        self.image_dir=image_dir
        self.image_file=image_file
        self.filename = self.image_dir + self.image_file
        self.position = position
        self.dot_color = dot_color
        self.dot_point = dot_point
        self.dot_radius = dot_radius
        self.dot_show = dot_show
        self.square_color = square_color
        self.square_show = square_show
        self.coordsys = coordsys
       
        self.pcoord  = self.coordsys.axes.coords_to_point(self.position[0],self.position[1])
        pc = [self.pcoord[0], self.pcoord[1]]
        op = self.coordsys.axes.coords_to_point(0,0)
        self.originPoint = [op[0], op[1]]
        
        self.position_vector = Arrow(start=self.originPoint, end=pc)
        self.position_history.append(self.position)  # first position
        print(self.position_history)
        self.image_height = image_height
        
        self.sprite = ImageMobject(self.filename,height=self.image_height) 
        self.dot = Dot(point=LEFT, radius=self.dot_radius,color=RED)
        self.outline = Square(side_length=self.sprite.height, color=self.square_color)
        
        self.setup()
     
    def setup(self):
        #self.sprite = ImageMobject(self.filename)
        self.sprite.generate_target()
        self.dot.generate_target()
        self.outline.generate_target()
        self.position_vector.generate_target()
        self.add(self.position_vector)
        
        # set positions 
        self.pcoord  = self.coordsys.axes.coords_to_point(self.position[0],self.position[1])
        
        #move everything
        self.sprite.move_to(self.pcoord)
        self.dot.move_to(self.pcoord)
        self.outline.move_to(self.pcoord)
       
        # add visible to group
        self.add(self.sprite)
        if self.dot_show : 
            self.add(self.dot)
        if self.square_show : 
            self.add(self.outline)
            
        #self.update_history()
            
    def update_history(self):
        prev = self.position_history[-1] # last in list so far 
        self.position_history.append(self.position)
        
        pc = self.coordsys.axes.coords_to_point(self.position[0],self.position[1])
        ppc = self.coordsys.axes.coords_to_point(prev[0],prev[1])
        
        d=(Dot(point=pc, radius=self.dot_radius/2,color=RED, opacity=0.1))
        l = Line(start=ppc, end=pc)

        return [ShowCreation(l),ShowCreation(d)]
        
        
    def ShowCreation(self):
        Animations=[]
        
        
        self.pcoord  = self.coordsys.axes.coords_to_point(self.position[0],self.position[1])
        pc = [self.pcoord[0], self.pcoord[1]]
        self.position_vector.target = Arrow(start=self.originPoint, end=pc)
        
        Animations.append(ShowCreation(self))
        Animations.append(MoveToTarget(self.position_vector))
        hanims = self.update_history()
        for a in hanims:
            Animations.append(a)
        
        print(self.position_history)

        return Animations
    
    def Move(self, targetPoint = np.array([5,5,0])):
        Animations=[]
        
        self.position = targetPoint
        
        self.pcoord  = self.coordsys.axes.coords_to_point(self.position[0],self.position[1])
        pc = [self.pcoord[0], self.pcoord[1]]
        
        self.dot.target.move_to(self.pcoord)
        self.sprite.target.move_to(self.pcoord)
        self.outline.target.move_to(self.pcoord)
        self.position_vector.target = Arrow(start=self.originPoint, end=pc)
        
        Animations.append(MoveToTarget(self.dot))
        Animations.append(MoveToTarget(self.sprite))
        if self.square_show : 
            Animations.append(MoveToTarget(self.outline))
            
        Animations.append(MoveToTarget(self.position_vector))
        
        hanims = self.update_history()
        for a in hanims:
            Animations.append(a)
        
        return Animations
        
    
# a simple coordinate system class
class CoordSystem2D(VGroup):
        def __init__(self,
                x_range = (-2, 10,1), y_range=(-1, 6, 1), 
                width=10, height=6,
                stroke_width=2, 
                stroke_color=GREY_A, 
                numbers_to_exclude=[0],
                font_size=12, 
                num_decimal_places=1,
                big_tick_numbers=[-2, 2],
                show_grid=True,
                **kwargs):
            super().__init__(**kwargs)
            # setup values to passed in vars/defaults
            self.stroke_color=stroke_color
            self.stroke_width=stroke_width
            self.num_decimal_places = num_decimal_places
            self.font_size=font_size
            self.width=width
            self.height=height
            self.numbers_to_exclude = numbers_to_exclude
            self.big_tick_numbers = big_tick_numbers
            self.x_range = x_range
            self.y_range = y_range
            self.show_grid = show_grid
            # setup axes mobject with these defaults
            self.setup()
            
        # call this to create the axes with set values
        def setup(self):
            grid = NumberPlane(
                background_line_style = {"stroke_color":GREY_B, "stroke_width":4, "stroke_opacity":0.1},
                axis_config = {"stroke_color":GREY_B, "stroke_width":4, "stroke_opacity":0.1}
                )
            self.axes = Axes(
                    x_range=self.x_range,
                    # y-axis ranges from -2 to 2 with a step size of 0.5
                    y_range=self.y_range,
                    # The axes will be stretched so as to match the specified
                    # height and width
                    height=self.height,
                    width=self.width,
                    axis_config=dict(
                        stroke_color=self.stroke_color,
                        stroke_width=self.stroke_width,
                        stroke_opacity=0.5,
                        numbers_to_exclude=self.numbers_to_exclude,
                    ),
            )
            self.axes.add_coordinate_labels(
                font_size=self.font_size,
                num_decimal_places=self.num_decimal_places,
            )
            if self.show_grid:
                self.add(grid)
            self.add(self.axes)

        # reset is used to start over
        def reset(self):
            self.remove(self.axes)
        
        
        
class testing(Scene):
    def construct(self):
        self.wait()
        c = CoordSystem2D()
        sp = Sprite(coordsys=c)
        sp2 = Sprite(coordsys=c, position=np.array([8,5,0]))
        
        self.play(ShowCreation(c))
        
        self.play(*sp.ShowCreation())
        self.play(*sp.Move(np.array([-2,0,0])))
        self.wait()
        
        self.play(*sp.Move(np.array([-2,2,0])))
        self.wait()
        
               
        self.play(*sp2.ShowCreation())
        self.play(*sp2.Move(np.array([8,4,0])))
        self.wait()
        self.play(*sp2.Move(np.array([7,4,0])))
        self.wait()
        self.play(*sp2.Move(np.array([6,4,0])))
        self.wait()

        

class CoordinateSystemExample(Scene):
    def construct(self):
        # Tex to color map
        t2c = {
            "x": RED,
            "y": GREEN,
            "z": BLUE,
        }
        # Configuration to pass along to each Tex mobject
        kw = dict(font_size=72, t2c=t2c)
        lines = VGroup(
            Tex("x", **kw),
            Tex("y", **kw),
            Tex("p = (x,y)", **kw),
            Tex(R"\vec{p}", **kw),
        )
        lines.arrange(DOWN, buff=LARGE_BUFF)

        axes = Axes(
            # x-axis ranges from -1 to 10, with a default step size of 1
            x_range=(-2, 2,0.5),
            # y-axis ranges from -2 to 2 with a step size of 0.5
            y_range=(-2, 2, 0.5),
            # The axes will be stretched so as to match the specified
            # height and width
            height=6,
            width=10,
            # Axes is made of two NumberLine mobjects.  You can specify
            # their configuration with axis_config
            axis_config=dict(
                stroke_color=GREY_A,
                stroke_width=2,
                numbers_to_exclude=[0],
            ),
            # Alternatively, you can specify configuration for just one
            # of them, like this.
            y_axis_config=dict(
                big_tick_numbers=[-2, 2],
            )
        )
        # Keyword arguments of add_coordinate_labels can be used to
        # configure the DecimalNumber mobjects which it creates and
        # adds to the axes
        axes.add_coordinate_labels(
            font_size=20,
            num_decimal_places=1,
        )
        self.add(axes)

        # Axes descends from the CoordinateSystem class, meaning
        # you can call call axes.coords_to_point, abbreviated to
        # axes.c2p, to associate a set of coordinates with a point,
        # like so:
        dot = Dot(color=RED)
        dot.move_to(axes.c2p(0, 0))
        self.wait()
        self.play(FadeIn(dot, scale=0.5))
        self.play(dot.animate.move_to(axes.c2p(1, 1)))
        # self.wait()
        # self.play(dot.animate.move_to(axes.c2p(5, 0.5)))
        # self.wait()

        # Similarly, you can call axes.point_to_coords, or axes.p2c
        # print(axes.p2c(dot.get_center()))

        # We can draw lines from the axes to better mark the coordinates
        # of a given point.
        # Here, the always_redraw command means that on each new frame
        # the lines will be redrawn
        h_line = always_redraw(lambda: axes.get_h_line(dot.get_left()))
        v_line = always_redraw(lambda: axes.get_v_line(dot.get_bottom()))
        h_line_label = lines[0].move_to(h_line.get_center())
        v_line_label = lines[1].move_to(v_line.get_center())
        self.play(ShowCreation(h_line))
        self.play(FadeIn(h_line_label))
        self.wait()
        self.play(ShowCreation(v_line))
        self.play(FadeIn(v_line_label))
         
        

