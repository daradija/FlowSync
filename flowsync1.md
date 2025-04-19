Un cruce simple, con vehículos que lo quieren atravesar perperndicularmente. En una única dirección.
En un porcentaje dado.
Se desea asociar la fase con relación al porcentaje.

Objetivos:

- Aritmética de eventos, como los AER (Adress event representation) de los spikes
- Que el reparto se ajuste a la densidad de vehículos
- Lenguaje de descripción de cruces, fuentes.

Desarrollo:
- Pseudogradiente en una PINN 100% física.

Debería modelar la llegada de vehículos en el cruce, considerando una distribución de Poisson para representar la aleatoriedad en los intervalos de tiempo entre llegadas. Esto permitirá simular escenarios realistas y ajustar dinámicamente las fases del semáforo según la densidad de tráfico.

Léxico en inglés:

Cruce: intersection
Movimiento: movement
Fase: phase
Semáforo: traffic light
Vehículo: vehicle   
Carretera: road
Punto de entrada: entry point
Punto de salida: exit point

Cada apertura tiene un tiempo.
Si no se puede ejecutar la salida se espera. y bloquea parte de la intersección.
Es mejor representar por metros. Velocidad y longitud del vehículo, con su distancia de parada y seguridad en marcha.

Los lanes? son una multiplicación de la capacidad. De momento en esta primera versión no se van a considerar.

Hay una negociación. Lo que te gustaría verter y lo que al final te permito verter.

Realmente el sistena se puede modelar como la distancia de vehículos en movimiento (con distancia de seguridad) Pero con un aunmente de la capacidad con la distancia en parada. 

La distancia se mide en metros.
La velocidad en km/h.
No usamos las unidades del SI. Sino las habituales en tráfico.

Si lo dibujo me aseguro la coherencia de manera visual.

Pixel por metro. Las medidas están en los Input y Output.

Hay un problema con el generador de poisson al tener en cuenta las medias físicas de los vehículos en movimiento. Si se solapan hay que desplazar el vehículo.

Por eficiencia se puede dar la lista de vehículos con sus distancias. El cruce, por ejemplo, sabiendo su tiempo, puede calcular cuantos entran en el cruce. Cuando se pone la luz verde y si está despejado.

El generador poisson podría tener un generador, tipo yield. Es muy cómodo como consumidor, y he de comunicar si puede o no puede entrar y hasta que momento he consumido.
Es como un analizador léxico, tengo caracteres en tentativa y consumo real. Lo lógico es que sea la propia carretera la que se ocupe de la responsabilidad de pretención, consumo. 

En vez del generador de poisson.
Teniendo en cuenta la capacidad de la intercepción.
Con la medida de los vehículos.
Podemos decidir por donde entran los próximos coches.
Según una probabilidad.

Generas un coche cada X tiempo y lo introduces al azar en una de las calles.

Tamaño medio de un coche en europa:
Según estudios recientes, el tamaño medio de un coche en Europa tiene aproximadamente:

- Longitud: 4.3 metros
- Anchura: 1.8 metros
- Altura: 1.5 metros

La distancia de seguridad recomendada entre vehículos en movimiento es de aproximadamente:
- 2 segundos de separación temporal (que a diferentes velocidades representa diferentes distancias)
- A 50 km/h: aproximadamente 28 metros
- A 30 km/h: aproximadamente 17 metros

En situación de parada (semáforo en rojo):
- Distancia entre vehículos: 1-2 metros
- Capacidad: aproximadamente 140-180 vehículos por kilómetro por carril

Hay dos puntos de vista, el cruce pide vehículos. 
O el vehículo intenta entrar.
Con la aritmética modular sería posible.
Pero ya no habría adaptación.

Vamos a pedir a la carretera que me de su previsión.

Quiero un generador de vehículos. Que meta según la proporción los vehículos por road 1 o road 2.
El vehículo se mete con push.

Hay tres eventos.
Dame vehículos hasta X tiempo.


Un semaforo se caracteriza por su:
ciclo, reparto y desfase.
En inglés:
cycle,split and offset.

Tengo dudas con la estructura de bifurcación.
Si se conecta directamente la carretera.

¿Qué ocurre cuando el tráfico se bifurca?
Es una intersección. 

Dentro puede tener una road...
En un futuro en las conexiones podremos poner bifurcaciones.

Cuando pasa de 50 km/h a 30 km/h se van añadiendo retrasos.
Para ello debo saber cuando la carretera se queda vacia para meter otra.
Y el get debe de esperar. Es por lo tanto el máximo entre el get y el quedarse libre.

Es raro porque al hacer un push, me indica cuando puede hacerse el próximo push.
Con eso basta. 
No saco aunque lleguen antes.
Hay un free input, y un free output.

Las carreteras son inelásticas.
Es decir tienen una capacidad ilimitada.

El freeInputTime se calcula con el de entrada del vehículo.

Hay que pensar en la interfaz gráfica.
El vehículo puede registrar las entradas y luego representar graficamente el movimiento.

El sensor está en el semáforo.
Debe cuadrar con el flujo.

Un objetivo era hacer el sistema autodiferncial. 

¿Cómo hace el sistema operativo?
Hay que insertar un coche. Pero cuando se llena sin salir ya no puede admitir mas entradas.
¿Cómo se simula la saturación?
¿por no mantener la distancia de seguridad?
Cuando no hay suficiente distancia de seguridad el tiempo de llegar a la salida aumenta. 

Pero aun me queda pensar en el orquestador.
Meto un coche y me dice cuando tengo que ejecutar el cruce.
La lógica es hacer el bash según la elasticidad posible.
Si en el otro extremo me hacen parár meterá retardo por saturación.

Cuando se ejecuta un semaforo no se sabe que la otra carretera no abierta se está saturando.
Hay que informarla de que no se está producciendo la entrada.

Se conduce a velocidad normal hasta llegar a la distancia de seguridad.

Las carreteras se ejecutan en paralelo hasta su capacidad con distancia de seguridad. 
A partir de ahí se ejecuta el extremo de salida.
Si se entapona, se puede ejecutar la entrada hasta el tiempo de entaponamiento.
Eso hará que la velocidad media disminuya.
Primero tienes que suprimir tiempos. Has de apretujar a los conductores.
Y llegado el caso has de impedir la entrada.

Podríamos ignorar el proceso de frenada. Haciendo que el nuevo lo asumiese todo. En teoría con una integral sería posible. O en base al frenazo y anteriores recalcular los tiempos de salida.

Sistema operativo:
La carretera cambia su posición de ejecucion con el cruce.

---

Podemos ejecutar un elemento hasta llegar a la capacidad de distancia de seguridad.
Y una vez alcanzado dicho punto hacemos un intercambio de punteros si la salida está por debajo.
Luego un problema secundario es la velocidad llegado a dicha saturación.

--- 

Si la saturación responde o no a la distancia de seguridad se lo podemos preguntar a Paco León. 
El tiempo extra de compactación se puede ejecutar en lote, dado que es un incremento de llegada al extremo y solo se ejecuta cuando hay capacidad de admitir un nuevo coche. 
Me pregunto si hay fórmula empirica. 
Hasta que esto no se modele nunca tendremos el comportamiento de los detectores modelados.
Sobre todo el concepto de ocupación. 
En cualquier caso, sería interesante pensar en la media de ocupación y si esta solo depende del número de coches previos y a la velocidad de entrada atenuada, por el bloqueo.
Y el número de coches previos, en el momento de entrada o en el momento de entrada solamente.

---


La semilla de azar también sería deseable controlarla para la reproductibidad.

Pero si mañana hay un swapping necesito azar.

---

Tengo que modelar las salidas de las carreteras de salidas.
Simplemente ejecuto el 100% de la cola.

Al sacar al 100% no sé como es la densidad. 

Vamos a graficar la curva.

```python
    def totalDistance(self,velocity):
        if velocity == 0:
            return 1.5+self.length
        if velocity <= 30:
            return 17
        if velocity <= 50:
            return 28
```
Esta función transforma de velocidad a distancia.

![](assets/17450457701739.jpg)
Es casi una línea recta.

La densidad de coches da la distancia de seguridad.
La distancia de seguridad da la velocidad.

Pero la densidad de coches depende del scheduler.
Yo puedo saber cuando llegue a la punta cuantos coches habrán salido.
Se puede calcular una densidad de coches a toro pasado.

Se sabe a ciencia cierta cuando entra y cuando sale un coche.

Me da igual el scheduler. La media va a ser correcta.
Si se adelantan por el scheduler no va a afectar.

Si velocidad es cero, se ha bloqueado por saturación.
Ejecuta los elementos con saturación.

---

Si se usa el coche saliente para establecer la velocidad el problema es que el nuevo coche no va a superar dicho tiempo.
A menos que si podría haber salido cuente.
El problema es la velocidad mínima.
Por densidad se puede deducir, pero no caigo ahora en la fórmula.

También podemos no poner el momento de llegada hasta sacar a un coche. 

Esto modelaría las velocidades ilegales, también.

