"""
The owner of park has a trouble with these piegons!
Please drive them out with your balls!
Tips:
Move with WASD
Shoot with left click
Some of them may not be driven at once
and DON'T hit citizens!

CopyRight:@Jeong GyongYun(github.com/yony1018) @vizard
"""
import viz
import vizfx
import vizconnect
import vizshape
import vizact
import vizcam
import vizinfo


NUM_BALLS			= 5 
BALL_SPEED			= 8 
vizinfo.InfoPanel()

viz.setMultiSample(4)
viz.fov(60)
viz.go()


#设置场景
lobby = vizfx.addChild('piazza.osgb')



#设置初始位置与视角倾斜
viz.MainView.setPosition([0,0,0])
viz.MainView.setEuler([0,0,0])

#设置第一人称视角
tracker = vizcam.addWalkNavigate(moveScale=2.0)
tracker.setPosition([0,1.8,0])
viz.link(tracker,viz.MainView)
viz.mouse.setVisible(False)


#增加准星

crosshair = viz.addTexQuad(viz.ORTHO, texture=viz.add('crosshair.png'), size=64)
viz.link( viz.Mouse , crosshair, srcFlag=viz.WINDOW_PIXELS )


#存储npc信息
balls = []
pigeons = []
people = []

#设置物理引擎
viz.phys.enable()
viz.phys.setGravity([0,-4,0])


#设置球体
for x in range(NUM_BALLS):
	ball = viz.addChild('beachball.osgb',pos=(0,0,-40),flags=viz.CACHE_CLONE)
	#设置刚性
	ball.collideSphere()
	ball.enable(viz.COLLIDE_NOTIFY)
	balls.append(ball)

#球体重置机制
nextBall = viz.cycle(balls)

#击发
def shootBall():
	ball = nextBall.next()

	#根据准星计算射出矢量
	line = viz.MainWindow.screenToWorld(viz.mouse.getPosition())
	line.length = BALL_SPEED

	#设置初始位置
	ball.setPosition(line.begin)

	#初始化球体参数
	ball.reset()
	ball.setVelocity(line.dir)

	#击发声音
	viz.playSound('gunshot.wav')

#左键触发
vizact.onmousedown(viz.MOUSEBUTTON_LEFT,shootBall)


#设置鸽子
import random

pigeons = []
for i in range(10):

    x = random.randint(-4,3)
    z = random.randint(4,8)
    yaw = random.randint(0,360)

    #加载鸽子
    pigeon = viz.addAvatar('pigeon.cfg')

    #设置位置姿势
    pigeon.setPosition([x,0,z])
    pigeon.setEuler([yaw,0,0])
    pigeon.state(1)

    #设置刚性
    pigeon.collideMesh()
    pigeon.disable(viz.DYNAMICS)
    
    pigeons.append(pigeon)

def pigeonsFeed():

    random_speed = vizact.method.setAnimationSpeed(0,vizact.randfloat(0.7,1.5))
    random_walk = vizact.walkTo(pos=[vizact.randfloat(-4,4),0,vizact.randfloat(3,7)])
    random_animation = vizact.method.state(vizact.choice([1,3],vizact.RANDOM))
    random_wait = vizact.waittime(vizact.randfloat(5.0,10.0))
    pigeon_idle = vizact.sequence( random_speed, random_walk, random_animation, random_wait, viz.FOREVER)

    for pigeon in pigeons:
        pigeon.addAction(pigeon_idle)
pigeonsFeed()



#设置owner
owner = viz.addAvatar('vcc_male2.cfg',pos=(-6.5,0,13.5),euler=(90,0,0))
owner.state(6)

#设置市民
male = viz.addAvatar('vcc_male.cfg')
male.setPosition([4.5, 0, 7])
male.setEuler([0,0,0])

female = viz.addAvatar('vcc_female.cfg')
female.setPosition([4.5,0,9])
female.setEuler([180,0,0])

#初始化 motion into 14（talking）
male.state(14)
female.state(14)


people.append(male)
people.append(female)
people.append(owner)

for person in people:
    #设置刚性
    person.collideMesh()
    person.disable(viz.DYNAMICS)

#碰撞
def oncollide(e):
    if e.obj2 == owner:
        textScreen1 = viz.addText('GAME OVER!',viz.SCREEN)
        textScreen1.alignment(viz.ALIGN_RIGHT_BOTTOM)
        textScreen1.setPosition([0.5,0.5,0])
        textScreen2 = viz.addText('Why you hit owner?!',viz.SCREEN)
        textScreen2.alignment(viz.ALIGN_RIGHT_BOTTOM)
        textScreen2.setPosition([0.8,0.2,0])
    if e.obj2 in pigeons:
        viz.playSound('quack.wav')
        e.obj2.setPosition([100,-100,100])
    if e.obj2 in people:
        e.obj2.state(9)
    viz.playSound('bounce.wav')
viz.callback(viz.COLLIDE_BEGIN_EVENT,oncollide)


def UpdateVelocity():
	for ball in balls:
		ball.setVelocity(viz.Vector(ball.getVelocity(),length=BALL_SPEED))
vizact.ontimer(0,UpdateVelocity)


#增加上帝视角
import viz
import vizact
import vizshape
import vizinfo

viz.setMultiSample(4)
viz.fov(60)
viz.go()


BirdEyeWindow = viz.addWindow()
BirdEyeWindow.fov(60)
BirdEyeWindow.visible(0,viz.SCREEN)
BirdEyeView = viz.addView()
BirdEyeWindow.setView(BirdEyeView)
BirdEyeView.setPosition([0,25,0])
BirdEyeView.setEuler([0,90,0])

#更新路线图
viz.startLayer(viz.LINE_STRIP)
viz.vertexColor(viz.YELLOW)
lines = viz.endLayer(parent=viz.ORTHO,scene=BirdEyeWindow)

lines.dynamic()

def UpdatePath():

    x,y,z = BirdEyeWindow.worldToScreen(viz.MainView.getPosition(),mode=viz.WINDOW_PIXELS)

    lx,ly,lz = lines.getVertex(-1)

    if x != lx or y != ly:
        lines.addVertex([x,y,0.0])

vizact.ontimer(0,UpdatePath)

vizact.onkeydown('',lines.clearVertices)



    