package main

import (
  "fmt"
  "math/rand"
  "os"
  "path/filepath"
  "strconv"
  "sync"
    "bufio"
    "strings"
)

// Estructura de datos para representar un proceso
type Proceso struct {
  Id            int
  Estado        string
  Contador      int
  Instrucciones []string
  EstadoES      string
}

// Estructura de datos para representar una cola de procesos
type ColaProcesos struct {
  Procesos []*Proceso
  mu       sync.Mutex
}

// Función para crear una cola de procesos vacía
func NuevaColaProcesos() *ColaProcesos {
  return &ColaProcesos{
    Procesos: make([]*Proceso, 0),
  }
}

// Función para agregar un proceso a una cola
func (c *ColaProcesos) Agregar(p *Proceso) {
  c.mu.Lock()
  defer c.mu.Unlock()
  c.Procesos = append(c.Procesos, p)
}

// Función para extraer el primer proceso de una cola
func (c *ColaProcesos) Extraer() *Proceso {
  c.mu.Lock()
  defer c.mu.Unlock()
  if len(c.Procesos) == 0 {
    return nil
  }

  p := c.Procesos[0]
  c.Procesos = c.Procesos[1:]
  return p
}

// Función para ejecutar una instrucción de un proceso
func EjecutarInstruccion(proceso *Proceso, instruccion string) {
  // Si la instrucción es de E/S, bloquear el proceso
  if instruccion[0] == 'E' {
    proceso.Estado = "Bloqueado"
    proceso.EstadoES = instruccion[1:]
  } else {
    // Si la instrucción es normal, incrementar el contador
    proceso.Contador++
  }
}

// Función para simular el funcionamiento del despachador
func SimularDespachador(procesos map[string]*ColaProcesos, n int, p float64, wg *sync.WaitGroup) {
  defer wg.Done()

  // Inicializar el contador de instrucciones
  contadorInstrucciones := 0
  var proceso *Proceso

  // Ciclo principal de la simulación
  for {
    var instruccion string
    // Si hay un proceso en estado "Listo", ejecutarlo
    if len(procesos["Listo"].Procesos) > 0 {
      // Extraer el primer proceso de la cola "Listo"
      proceso = procesos["Listo"].Extraer()

      // Ejecutar la siguiente instrucción del proceso
      if proceso.Contador < len(proceso.Instrucciones) {
        instruccion := proceso.Instrucciones[proceso.Contador]
        EjecutarInstruccion(proceso, instruccion)
      }
      // Si la instrucción es de finalización, terminar el proceso
      if instruccion == "F" {
        proceso.Estado = "Finalizado"
      }

      // Si el proceso está bloqueado, agregarlo a la cola "Bloqueado"
      if proceso.Estado == "Bloqueado" {
        procesos["Bloqueado"].Agregar(proceso)
      }
    }

    // Incrementar el contador de instrucciones
    contadorInstrucciones++

    // Si el proceso en ejecución finalizó, continuar con el siguiente
    if proceso.Estado == "Finalizado" {
      continue
    }

    // Si el proceso en ejecución está bloqueado, continuar con el siguiente
    if proceso.Estado == "Bloqueado" {
      continue
    }

    // Si el proceso en ejecución ha ejecutado n instrucciones, cambiarlo a estado "Listo"
    if contadorInstrucciones >= n {
      proceso.Estado = "Listo"
      procesos["Listo"].Agregar(proceso)
      contadorInstrucciones = 0
    }

    // Si el proceso en ejecución tiene una probabilidad p de finalizar antes de tiempo, finalizarlo
    if rand.Float64() < p {
      proceso.Estado = "Finalizado"
    }
  }
}

func EscribirTraza(procesos []*Proceso) {
  // Obtener el directorio del programa
  dir, err := filepath.Abs(filepath.Dir(os.Args[0]))
  if err != nil {
    fmt.Println("Error al obtener el directorio del programa:", err)
    return
  }

  // Definir la ubicación del archivo de salida
  ubicacion := filepath.Join(dir, "salida.txt")

  // Crear el archivo de salida
  file, err := os.Create(ubicacion)
  if err != nil {
    fmt.Println("Error al crear el archivo:", err)
    return
  }
  defer file.Close()

  // Escribir la cabecera del archivo
  _, err = file.WriteString("Proceso\tEstado\tInstrucciones\n")
  if err != nil {
    fmt.Println("Error al escribir en el archivo:", err)
    return
  }

  // Escribir la traza de ejecución de cada proceso
  for _, p := range procesos {
    for _, instruccion := range p.Instrucciones {
      // Verificar si hay instrucciones antes de acceder a ellas
      if len(instruccion) > 0 && instruccion[0] != 'E' {
        _, err = file.WriteString(fmt.Sprintf("%d\t%s\t%s\n", p.Id, p.Estado, instruccion))
        if err != nil {
          fmt.Println("Error al escribir en el archivo:", err)
          return
        }
      }
    }
  }
}

func main() {
  if len(os.Args) < 4 {
    fmt.Println("Por favor, proporciona tres argumentos de línea de comandos")
    return
  }

  // Leer los parámetros de entrada
  n, err := strconv.Atoi(os.Args[1])
  if err != nil {
    fmt.Println("Error al leer el parámetro n:", err)
    return
  }

  p, err := strconv.ParseFloat(os.Args[2], 64)
  if err != nil {
    fmt.Println("Error al leer el parámetro p:", err)
    return
  }

  //archivoProcesos := os.Args[3]

  // Leer los procesos
  procesos := LeerProcesos("procesos.txt")
  if procesos == nil {
    return
  }

  // Inicializar las colas de procesos
  procesosListo := NuevaColaProcesos()
  procesosBloqueado := NuevaColaProcesos()
  procesosFinalizado := NuevaColaProcesos()

  procesosMap := map[string]*ColaProcesos{
    "Listo":      procesosListo,
    "Bloqueado":   procesosBloqueado,
    "Finalizado": procesosFinalizado,
  }

  // Agregar los procesos a la cola "Listo" inicialmente
  for _, proceso := range procesos {
    procesosListo.Agregar(proceso)
  }

  var wg sync.WaitGroup

  // Simular el funcionamiento del despachador en una goroutine
  wg.Add(1)
  go SimularDespachador(procesosMap, n, p, &wg)

  // Esperar a que la simulación termine
  wg.Wait()

  // Escribir la traza de ejecución
  EscribirTraza(procesos)
}

// Agrega la función LeerProcesos según tus necesidades
func LeerProcesos(archivoProcesos string) []*Proceso {
  // Abrir el archivo
  file, err := os.Open(archivoProcesos)
  if err != nil {
    fmt.Println("Error al abrir el archivo:", err)
    return nil
  }
  defer file.Close()


  var procesos []*Proceso

  // Leer cada línea del archivo
  scanner := bufio.NewScanner(file)
  for scanner.Scan() {
    linea := scanner.Text()
    campos := strings.Split(linea, ",")

    // Convertir campos según sea necesario
    id, _ := strconv.Atoi(campos[0])
    contador, _ := strconv.Atoi(campos[2])

    // Separar las instrucciones utilizando strings.Split y convertir a []string
    instrucciones := strings.Split(campos[3], ";")
    instruccionesStr := make([]string, len(instrucciones))
    for i, v := range instrucciones {
      instruccionesStr[i] = v
    }

    // Crear un nuevo proceso y agregarlo a la lista
    proceso := &Proceso{
      Id:            id,
      Estado:        campos[1],
      Contador:      contador,
      Instrucciones: instruccionesStr,
      EstadoES:      "",
    }
    procesos = append(procesos, proceso)
  }

  if err := scanner.Err(); err != nil {
    fmt.Println("Error al leer el archivo:", err)
    return nil
  }

  return procesos
}
