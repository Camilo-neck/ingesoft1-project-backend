interface Usuario {
    id: number;
    nombre: string;
    tipoUsuario: "Estudiante" | "Propietario" | "Administrador"
    urlFotoPerfil: string;
    password: string;
    chazasPropias?: Chaza[]
}

interface Mensaje{
    id: number;
    contenido: string;
    fecha: Date;
    usuario: Usuario
}

interface Comentario{
    id: number;
    contenido: string;
    fecha: Date;
    usuario: Usuario;
    estrellas: number;
    upvotes: number;
}

interface Mensaje{
    id: number;
    contenido: string;
    fecha: Date;
    Estudiante: Usuario
}


interface Reporte{
    id: number;
    contenido: string;
    fecha: Date;
    usuario: Usuario
    estaResuelto: boolean;
}

interface Chaza{
    id: number;
    nombre: string;
    ubicacion: string;
    descripcion: string;
    urlImagen: string[];
    telefono: string;
    horario: Date;
    propietario: Usuario;
    comentarios: Comentario[];
    calificacion: number;
    urlFotoChaza: string;
    reportes: Reporte[]
}

interface Categoria{
    id: number;
    nombre: string;
    chazas: Chaza[]
}