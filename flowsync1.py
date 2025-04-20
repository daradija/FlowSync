import numpy as np

class Phase:
    def __init__(self,intersection,split ):
        self.intersection = intersection
        self.split = split
        self.io=[]

    def open(self, input, output,distance,velocity):
        self.io.append((input, output, Road(distance, velocity,self.intersection.name)))


class Intersection:
    def __init__(self, inputs, outputs,phases, name=None):
        self.name = name
        self.input = inputs
        self.output = outputs
        self.phases = [Phase(self,0.5) for _ in range(phases)]
        self.offset = 0
        self.cycle = 90
        self.t = 0

    def run(self):
        second_cicle=(self.t - self.offset)% self.cycle
        phase=second_cicle/self.cycle

        split=0
        can0=True
        for p in self.phases:
            change=split+p.split
            if phase < change:
                changet=self.t
                # print("Change phase", changet)
                for intersection in p.io:
                    input=self.input[intersection[0]]
                    output=self.output[intersection[1]]
                    road=intersection[2]
                    if not road.full():
                        changet=(change-split)*self.cycle+self.t
                        for t,v in input.get(max(self.t,road.freeInputTime),changet):
                            if v==None:
                                can=False
                                changet=t
                                can0=False
                                break
                            else:
                                can=road.push(t,v)
                                if not can:
                                    changet=road.freeInputTime
                                    can0=False
                                    break
                               
                            if road.freeInputTime > changet:
                                break        
                    # Empty the intersection
                    if not output.full():
                        for t,v in road.get(0):
                            can=output.push(t,v)
                            if not can:
                                can0=False
                                break
                    # for p in self.phases:
                    #     for intersection in p.io:
                    #         intersection[2].freeInputTime=road.freeInputTime
                if self.t==changet:
                    return False
                self.t=changet
                break
            split=change
        return can0

class Road:
    def __init__(self, length, velocity, name=None):
        self.name = name
        self.length = length
        self.velocity = velocity
        self.lastVelocity = velocity
        self.queue=[]
        self.freeInputTime=0
        self.freeOutputTime=0
        self.queueLength=0

    def safetyDistance(self):
        s= max(3, (self.velocity-self.lastVelocity)/50*(28-4.2))
        return s

    def velocityms(self):
        # Convert velocity from km/h to m/s
        return self.velocity / 3.6
    
    def full(self):
        f= self.queueLength+len(self.queue)*self.safetyDistance()>self.length
        return f
    
    def push(self, time, vehicle=None):
        if vehicle!=None and self.full():
            raise Exception("Queue is full")
        if time < self.freeInputTime:
            time=self.freeInputTime
        # Hay que hallar a que hora se admite una nueva entrada
        # Es el tiempo de entrada a la velocidad de la via
        # v= e/t => t=e/v

        if vehicle!=None:
            vehicle.log.append((time,"push",self.name))
            self.freeInputTime=time+vehicle.totalDistance(self.velocity)/self.velocityms()
            # A que hora sale cabeza y cola 
            self.queue.append((time+self.length/self.velocityms(), vehicle))
            self.queueLength+=vehicle.length
            # v= e/t => t=e/v    
        else:
            self.freeInputTime=time
        self.freeOutputTime=self.freeInputTime+self.length/self.velocityms()
        return not self.full()
        
    def get(self, time, time_to=None):
        if len(self.queue)==0:
            yield (max(self.freeOutputTime,time), None)
            return
        # puede ocurrir tres cosas: delante, en medio, detrás.
        waiting=0
        if self.queue[0][0] < time:
            waiting=time-self.queue[0][0]

       
        while True:
            if len(self.queue)==0:
                yield (self.freeOutputTime+waiting, None)
                return
            q=self.queue[0]
            if time_to==None or q[0]+waiting <time_to:
                self.queue.pop(0)
                self.lastVelocity=0.9*self.lastVelocity+0.1*self.length/(q[0]+waiting-q[1].log[-1][0])*3.6
                print(self.name,"lastVelocity",self.lastVelocity)
                q[1].log.append((q[0]+waiting,"get",self.name))
                self.queueLength-=q[1].length
                yield (q[0]+waiting,q[1])
            else:
                break


    
class Vehicle:
    def __init__(self, length):
        self.length = length
        self.log=[]

    def totalDistance(self,velocity):
        d= velocity/50*28
        return max(d, self.length+1.5)
        # if velocity == 0:
        #     return 1.5+self.length
        # if velocity <= 30:
        #     return 17
        # if velocity <= 50:
        #     return 28

        

class Executor:
    def __init__(self, f):

        self.f = f

class Sensor:
    def __init__(self, road):
        self.road = road
        self.intensidad=[]
        self.ocupacion=[]
        self.intervalo=5*60
    
    def addVehicle(self, v):
        for t,fname,name in v.log:
            if name==self.road.name:
                if fname=="push":
                    tin=t
                if fname=="get":
                    for i in range(1000):
                        if len(self.intensidad)<=i:
                            self.intensidad.append(0)
                            self.ocupacion.append(0)
                        if t<(i+1)*self.intervalo:
                            self.intensidad[i]+=1
                            # tiempo de ocupación.
                            # velocidad= e/t 
                            velocity=self.road.length/(t-tin)
                            # velocitykms=velocity*3.6
                            # print("velocidad",velocitykms)
                            # t=e/v
                            # ocupación= t/intervalo
                            self.ocupacion[i]+=v.length/velocity/self.intervalo
                            break
                    

    def study(self):
        intervalo=[]
        for i in range(len(self.intensidad)):
            intervalo.append((self.intensidad[i],self.ocupacion[i]))

        # sort by ocupacion
        intervalo.sort(key=lambda x: x[1], reverse=True)
        # top 5%
        top5=int(len(intervalo)*0.05)
        intervalo5=intervalo[:top5]

        top33=int(len(intervalo)*0.33)
        intervalo33=intervalo[:top33]

        # promedia intensidad
        print(f"Intensidad top5%: {sum([x[0] for x in intervalo5])/top5:.0f}({sum([x[1] for x in intervalo5]):.0f}%)")
        print(f"Intensidad top33%: {sum([x[0] for x in intervalo33])/top33:.0f}({sum([x[1] for x in intervalo33]):.0f}%)")
        print()


def main():
    road0= Road(100, 50,name="road0")
    road1= Road(100, 50,name="road1")

    road3= Road(100, 50,name="road3")
    road4= Road(100, 50,name="road4")

    # Create an intersection with 2 inputs and 2 outputs
    intersection = Intersection([road0,road1], [road3,road4],2,name="intersection")


    intersection.phases[0].open(0,0,5,30)
    intersection.phases[1].open(1,1,5,30)

    inCars=0
    outCars=0
    time=0
    def insert():
        nonlocal time, inCars
        if time>60*60*10: # 1 hour of simulation
            time+=60
            road0.push(time)
            road1.push(time)
            return False
        
        road=None
        if np.random.random() < 0.5:
            road=road0
        else:
            road=road1

        if road.full():
            return False

        vehicle=Vehicle(np.random.normal(4.2,1))
        inCars+=1
        r=road.push(time,vehicle)
        #print("Vehicles in ",road.name,len(road.queue))
        # v=e/t => t=e/v
        road_intersection=intersection.phases[0].io[0][2]
        time+= vehicle.totalDistance(road_intersection.velocity)/road_intersection.velocityms()
        return r
    
    s=Sensor(road0)
    #s=Sensor(intersection.phases[0].io[0][2])

    def remover():
        nonlocal outCars
        for t,v in road3.get(0):
            if v==None:
                break
            # for l in v.log:
            #     print(l)
            # print()
            outCars+=1
            s.addVehicle(v)
        for t,v in road4.get(0):
            if v==None:
                break
            # for l in v.log:
            #     print(l)
            # print()
            outCars+=1
            s.addVehicle(v)
        
        return False

    programa=[
        insert,
        intersection.run,
        remover,
    ]
    ip=0
    while True:
        while programa[ip]():
            pass
        ip=(ip+1)%len(programa)
        if outCars==inCars:
            break
    s.study()

if __name__ == "__main__":
    main()