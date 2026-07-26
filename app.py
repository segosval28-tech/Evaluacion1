from datetime import datetime
from pathlib import Path
import importlib.util

import numpy as np
import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent


def cargar_modulo_externo(nombre_modulo, nombres_archivo):
    rutas_busqueda = [BASE_DIR, BASE_DIR.parent]
    for carpeta in rutas_busqueda:
        for nombre_archivo in nombres_archivo:
            ruta = carpeta / nombre_archivo
            if ruta.exists():
                spec = importlib.util.spec_from_file_location(nombre_modulo, ruta)
                modulo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(modulo)
                return modulo

        for ruta in carpeta.glob("*clases_proyecto1.py"):
            spec = importlib.util.spec_from_file_location(nombre_modulo, ruta)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            return modulo

    archivos = ", ".join(nombres_archivo)
    raise FileNotFoundError(f"No se encontro la libreria externa: {archivos}")


funciones = cargar_modulo_externo(
    "libreria_funciones_proyecto1",
    ["libreria_funciones_proyecto1.py"],
)
clases = cargar_modulo_externo(
    "libreria_clases_proyecto1",
    ["libreria_clases_proyecto1.py", "librería_clases_proyecto1.py"],
)

calcular_margen_neto = funciones.calcular_margen_neto
InventarioProducto = clases.InventarioProducto


st.set_page_config(
    page_title="Gestion de Exportaciones",
    page_icon="EX",
    layout="wide",
)


st.markdown(
    """
    <style>
        :root {
            --navy: #082f49;
            --blue: #0f6ea8;
            --teal: #0f766e;
            --cyan: #22d3ee;
            --gold: #f59e0b;
            --ink: #102033;
            --muted: #64748b;
            --line: #d8e1ec;
            --paper: #ffffff;
            --soft: #f5f9fd;
        }
        .stApp {
            background:
                radial-gradient(circle at 8% 4%, rgba(34, 211, 238, 0.18), transparent 30%),
                radial-gradient(circle at 92% 12%, rgba(15, 118, 110, 0.16), transparent 28%),
                linear-gradient(180deg, #eef7fb 0%, #f8fafc 48%, #eef4f8 100%);
            color: var(--ink);
        }
        .main .block-container {
            max-width: 1180px;
            padding-top: 1.6rem;
            padding-bottom: 2rem;
        }
        
        /* --- ESTILOS DEL SIDEBAR --- */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #062338 0%, #0b3a53 48%, #062338 100%);
        }
        
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label {
            color: #eaf6fb !important;
        }

        /* ===== Streamlit 1.59 ===== */

        /* Texto del label */
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] label *,
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stSelectbox label *,
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"],
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] *{
            color:#ffffff !important;
            -webkit-text-fill-color:#ffffff !important;
            font-weight:700 !important;
        }
        
        /* Texto del valor seleccionado */
        [data-testid="stSidebar"] div[data-baseweb="select"] [data-value]{
            color:#0f172a !important;
            -webkit-text-fill-color:#0f172a !important;
        }

        /* --- CORRECCIÓN DEL SELECTBOX EN LA SIDEBAR --- */
        [data-testid="stSidebar"] div[data-baseweb="select"] > div {
            min-height: 40px;
            border: 1px solid rgba(34, 211, 238, 0.38) !important;
            border-radius: 8px !important;
            background-color: #ffffff !important;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.12);
        }

        [data-testid="stSidebar"] div[data-baseweb="select"] p,
        [data-testid="stSidebar"] div[data-baseweb="select"] span,
        [data-testid="stSidebar"] div[data-baseweb="select"] div {
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
            opacity: 1 !important;
            font-weight: 700 !important;
        }
        
        [data-testid="stSidebar"] input {
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
        }

        [data-testid="stSidebar"] div[data-baseweb="select"] svg {
            fill: #0f766e !important;
            color: #0f766e !important;
        }
       /* ---------------------------------------------- */

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] label p {
            color: #ffffff !important;
            font-weight: 700 !important;
            letter-spacing: 0;
        }
        .hero-box {
            position: relative;
            padding: 28px;
            border-radius: 8px;
            background:
                linear-gradient(120deg, rgba(8, 47, 73, 0.98), rgba(15, 110, 168, 0.93), rgba(15, 118, 110, 0.90)),
                repeating-linear-gradient(45deg, rgba(255, 255, 255, 0.10) 0, rgba(255, 255, 255, 0.10) 1px, transparent 1px, transparent 18px);
            color: white;
            margin-bottom: 22px;
            box-shadow: 0 24px 60px rgba(8, 47, 73, 0.25);
            overflow: hidden;
        }
        .hero-box::after {
            content: "";
            position: absolute;
            top: -70px;
            right: -60px;
            width: 240px;
            height: 240px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.13);
        }
        .hero-box h1 {
            color: white;
            margin-bottom: 8px;
            font-size: 2.45rem;
            line-height: 1.08;
            letter-spacing: 0;
        }
        .hero-box p {
            color: rgba(255,255,255,0.88);
            margin-bottom: 0;
            max-width: 760px;
            line-height: 1.55;
        }
        .info-box {
            padding: 18px;
            border: 1px solid rgba(216, 225, 236, 0.92);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.88);
            box-shadow: 0 16px 38px rgba(15, 23, 42, 0.08);
            backdrop-filter: blur(12px);
        }
        .active-section-box {
            margin-top: 12px;
            padding: 12px 13px;
            border: 1px solid rgba(34, 211, 238, 0.32);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.10);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.10);
        }
        .active-section-box span {
            display: block;
            color: rgba(234, 246, 251, 0.72) !important;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0;
            text-transform: uppercase;
        }
        .active-section-box strong {
            display: block;
            margin-top: 4px;
            color: #ffffff !important;
            font-size: 17px;
            line-height: 1.2;
        }
        h1, h2, h3 {
            color: #0f2338;
            letter-spacing: 0;
        }
        div[data-testid="stMetric"] {
            padding: 16px 18px;
            border: 1px solid rgba(216, 225, 236, 0.92);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.92);
            box-shadow: 0 14px 32px rgba(15, 23, 42, 0.07);
        }
        div[data-testid="stMetric"] label {
            color: var(--muted);
            font-weight: 800;
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(216, 225, 236, 0.92);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
        }
        div[data-testid="stForm"] {
            padding: 18px;
            border: 1px solid rgba(216, 225, 236, 0.92);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.88);
            box-shadow: 0 16px 38px rgba(15, 23, 42, 0.07);
        }
        .stTextInput input,
        .stNumberInput input {
            border-radius: 8px !important;
            border-color: #cbd5e1 !important;
            background-color: #fbfdff !important;
            transition: box-shadow 160ms ease, border-color 160ms ease, background-color 160ms ease;
        }
        .stTextInput input:focus,
        .stNumberInput input:focus {
            border-color: var(--teal) !important;
            box-shadow: 0 0 0 4px rgba(15, 118, 110, 0.13) !important;
            background-color: #ffffff !important;
        }
        div.stButton > button,
        div[data-testid="stFormSubmitButton"] button {
            position: relative;
            min-height: 44px;
            border: 0;
            border-radius: 8px;
            color: #ffffff;
            font-weight: 800;
            background: linear-gradient(135deg, var(--navy), var(--blue) 55%, var(--teal));
            box-shadow: 0 14px 28px rgba(15, 110, 168, 0.24);
            transition: transform 170ms ease, box-shadow 170ms ease, filter 170ms ease;
            overflow: hidden;
        }
        div.stButton > button:hover,
        div[data-testid="stFormSubmitButton"] button:hover {
            color: #ffffff;
            transform: translateY(-2px);
            filter: saturate(1.08);
            box-shadow: 0 18px 34px rgba(15, 110, 168, 0.31);
        }
        div[data-testid="stTabs"] button {
            border-radius: 8px 8px 0 0;
            font-weight: 800;
        }
        .stAlert {
            border-radius: 8px;
        }
        /* Etiquetas de formularios en negrita */
        div[data-testid="stForm"] label p,
        .stTextInput label p,
        .stSelectbox label p,
        .stNumberInput label p {
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            color: #0f2338 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def inicializar_estado():
    valores_iniciales = {
        "movimientos_exportacion": [],
        "embarques_exportacion": [],
        "historico_margen": [],
        "productos_exportacion": [],
        "editando_codigo": None,  # Variable de estado para controlar la edición en el CRUD
    }
    for clave, valor in valores_iniciales.items():
        if clave not in st.session_state:
            st.session_state[clave] = valor


def mostrar_dataframe(datos, mensaje_vacio):
    if datos:
        st.dataframe(pd.DataFrame(datos), use_container_width=True, hide_index=True)
    else:
        st.info(mensaje_vacio)


def crear_registro_producto(codigo, nombre, costo, precio, stock_actual, stock_minimo):
    producto = InventarioProducto(nombre, costo, precio, stock_actual, stock_minimo)
    resumen = producto.resumen()
    return {
        "Codigo": codigo.strip().upper(),
        "Producto": resumen["producto"],
        "Costo unitario USD": round(costo, 2),
        "Precio exportacion USD": round(precio, 2),
        "Stock actual": stock_actual,
        "Stock minimo": stock_minimo,
        "Valor inventario USD": resumen["valor_inventario"],
        "Margen unitario USD": resumen["margen_unitario"],
        "Margen %": resumen["margen_pct"],
        "Necesita reposicion": "Si" if resumen["necesita_reposicion"] else "No",
    }


def pagina_home():
    st.markdown(
        """
        <div class="hero-box">
            <h1>Sistema de Gestion de Exportaciones</h1>
            <p>Aplicacion Streamlit para controlar costos, embarques, rentabilidad e inventario exportable.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1.2, 0.8])

    with col1:
        st.subheader("Presentacion del proyecto")
        st.write(
            "Este proyecto aplica fundamentos de Python a un flujo real del area de "
            "exportaciones: desde la coordinacion logistica para trasladar carga al "
            "terminal maritimo o aereo, hasta el seguimiento de operaciones y entrega "
            "del producto al cliente final en el extranjero."
        )
        st.markdown(
            """
            **Objetivo:** construir una aplicacion clara y funcional que permita registrar
            informacion operativa, calcular resultados financieros y administrar productos
            asociados a exportaciones.
            """
        )

    with col2:
        st.markdown(
            """
            <div class="info-box">
                <h3>Datos generales</h3>
                <p><strong>Estudiante:</strong> Escribe aqui tu nombre completo</p>
                <p><strong>Modulo:</strong> Python Fundamentals</p>
                <p><strong>Curso:</strong> Python for Analytics</p>
                <p><strong>Anio:</strong> 2026</p>
                <p><strong>Perfil:</strong> Gestion logistica de exportaciones</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Tecnologias utilizadas")
    st.write("Python, Streamlit, Pandas, NumPy, funciones externas, clases externas y st.session_state.")

    st.subheader("Secciones de la aplicacion")
    st.markdown(
        """
        - **Ejercicio 1:** flujo de caja de una operacion de exportacion usando listas.
        - **Ejercicio 2:** registro de embarques con arrays de NumPy y DataFrame.
        - **Ejercicio 3:** calculo de margen neto usando una funcion externa.
        - **Ejercicio 4:** CRUD de productos exportables usando una clase externa.
        """
    )


def ejercicio_1():
    st.title("Ejercicio 1 - Flujo de caja con listas")
    st.markdown(
        "Registro de ingresos y gastos asociados a una operacion de exportacion. "
        "Los movimientos se guardan en una lista dentro de `st.session_state`."
    )

    with st.form("form_movimiento", clear_on_submit=True):
        col1, col2, col3 = st.columns([1.4, 1, 1])
        concepto = col1.selectbox(
            "Concepto del movimiento",
            [
                "Cobro de factura comercial",
                "Adelanto de cliente extranjero",
                "Trámite de DAM",
                "Comisión de agencia de aduanas",
                "Pagos por Vistos Buenos (VoBo)",
                "Emisión de BL / AWB",
                "Flete interno",
                "Servicios de almacenaje",
                "Movilización de contenedor",
                "Pesaje y transmisión VGM",
                "Flete marítimo internacional",
                "Flete aéreo internacional",
                "Póliza de seguro de carga",
                "Drawback",
                "Otros",
            ],
        )
        tipo = col2.selectbox("Tipo de movimiento", ["Ingreso", "Gasto"])
        categoria = col3.selectbox(
            "Categoria",
            [
                "Venta internacional",
                "Transporte interno",
                "Terminal",
                "Agente de aduanas",
                "Flete internacional",
                "Documentos",
                "Otros",
            ],
        )
        valor = st.number_input("Valor USD", min_value=0.0, step=10.0, format="%.2f")
        agregar = st.form_submit_button("Agregar movimiento")

    if agregar:
        if valor <= 0:
            st.error("El valor debe ser mayor que cero.")
        else:
            st.session_state.movimientos_exportacion.append(
                {
                    "Concepto": concepto,
                    "Tipo": tipo,
                    "Categoria": categoria,
                    "Valor USD": round(valor, 2),
                }
            )
            st.success("Movimiento agregado correctamente.")

    mostrar_dataframe(
        st.session_state.movimientos_exportacion,
        "Aun no hay movimientos registrados.",
    )

    movimientos = st.session_state.movimientos_exportacion
    total_ingresos = sum(m["Valor USD"] for m in movimientos if m["Tipo"] == "Ingreso")
    total_gastos = sum(m["Valor USD"] for m in movimientos if m["Tipo"] == "Gasto")
    saldo = total_ingresos - total_gastos

    col1, col2, col3 = st.columns(3)
    col1.metric("Total ingresos", f"USD {total_ingresos:,.2f}")
    col2.metric("Total gastos", f"USD {total_gastos:,.2f}")
    col3.metric("Saldo final", f"USD {saldo:,.2f}")

    if movimientos:
        if saldo >= 0:
            st.success("El flujo de caja esta a favor.")
        else:
            st.error("El flujo de caja esta en contra.")

    if st.button("Limpiar movimientos"):
        st.session_state.movimientos_exportacion = []
        st.rerun()


def ejercicio_2():
    st.title("Ejercicio 2 - Registro con NumPy, arrays y DataFrame")
    st.markdown(
        "Registro de embarques de exportacion. La informacion se almacena como registros, "
        "se transforma en arrays de NumPy y luego se presenta como DataFrame."
    )

    with st.form("form_embarque", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        producto = col1.selectbox(
            "Estilo de prenda",
            [
                "Camisas",
                "Tank",
                "T-Shirt Manga corta",
                "T-Shirt Manga larga",
                "T-shirt con estampado",
                "T-shirt con bordado",
                "T-shirt sublimado",
                "Short",
            ],
        )
        cliente = col2.selectbox(
            "Cliente",
            [
                "Lacoste",
                "Lululemon",
                "Theory",
                "Banana Republic",
                "Skechers",
                "Allbirs",
            ],
        )
        pais = col3.selectbox(
            "Pais destino",
            [
                "USA",
                "Canadá",
                "China",
                "Netherlands",
                "Singapore",
                "Reino Unido",
                "Mexico",
                "Argentina",
                "Brasil",
                "Vietnan",
                "Australia",
            ],
        )

        col4, col5, col6 = st.columns(3)
        via = col4.selectbox("Via de transporte", ["Maritimo", "Aereo"])
        incoterm = col5.selectbox("Incoterm", ["FOB", "CFR", "CIF", "DAP", "DDP", "EXW"])
        cantidad = col6.number_input("Cantidad", min_value=1, step=1)

        precio = st.number_input("Precio unitario USD", min_value=0.0, step=1.0, format="%.2f")
        agregar = st.form_submit_button("Agregar embarque")

    if agregar:
        if precio <= 0:
            st.error("El precio unitario debe ser mayor que cero.")
        else:
            total = cantidad * precio
            st.session_state.embarques_exportacion.append(
                {
                    "Producto": producto,
                    "Cliente": cliente,
                    "Pais destino": pais,
                    "Via": via,
                    "Incoterm": incoterm,
                    "Cantidad": cantidad,
                    "Precio unitario USD": round(precio, 2),
                    "Total exportado USD": round(total, 2),
                }
            )
            st.success("Embarque agregado correctamente.")

    registros = st.session_state.embarques_exportacion
    if registros:
        productos = np.array([r["Producto"] for r in registros])
        clientes = np.array([r["Cliente"] for r in registros])
        paises = np.array([r["Pais destino"] for r in registros])
        vias = np.array([r["Via"] for r in registros])
        incoterms = np.array([r["Incoterm"] for r in registros])
        cantidades = np.array([r["Cantidad"] for r in registros])
        precios = np.array([r["Precio unitario USD"] for r in registros])
        totales = cantidades * precios

        df = pd.DataFrame(
            {
                "Producto": productos,
                "Cliente": clientes,
                "Pais destino": paises,
                "Via": vias,
                "Incoterm": incoterms,
                "Cantidad": cantidades,
                "Precio unitario USD": precios,
                "Total exportado USD": totales,
            }
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Embarques registrados", len(df))
        col2.metric("Unidades exportadas", f"{int(cantidades.sum()):,}")
        col3.metric("Valor total exportado", f"USD {totales.sum():,.2f}")
    else:
        st.info("Aun no hay embarques registrados.")

    if st.button("Limpiar embarques"):
        st.session_state.embarques_exportacion = []
        st.rerun()


def ejercicio_3():
    st.title("Ejercicio 3 - Funcion externa")
    st.markdown(
        "Uso de una funcion desde `libreria_funciones_proyecto1.py`. "
        "La funcion seleccionada calcula el margen neto de una operacion de exportacion."
    )

    funcion = st.selectbox(
        "Selector de funcion",
        ["calcular_margen_neto - Rentabilidad de exportacion"],
    )

    with st.form("form_margen"):
        operacion = st.text_input("Operacion o referencia (Cliente-Semana-Modo_envío)", placeholder="Ej. LACOSTE-SEM24-AEREO")
        col1, col2 = st.columns(2)
        ingresos = col1.number_input("Ingresos por venta internacional USD", min_value=0.0, step=100.0)
        costos = col2.number_input("Costo del producto USD", min_value=0.0, step=100.0)
        col3, col4 = st.columns(2)
        gastos = col3.number_input("Gastos logisticos y operativos USD", min_value=0.0, step=50.0)
        impuestos = col4.number_input("Impuestos o tasas USD", min_value=0.0, step=10.0)
        ejecutar = st.form_submit_button("Ejecutar funcion")

    if ejecutar:
        if not operacion.strip():
            st.error("Ingrese una referencia de operacion.")
        else:
            try:
                resultado = calcular_margen_neto(ingresos, costos, gastos, impuestos)
                fila = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Operacion": operacion.strip(),
                    "Funcion": funcion.split(" - ")[0],
                    "Ingresos USD": round(ingresos, 2),
                    "Costos USD": round(costos, 2),
                    "Gastos USD": round(gastos, 2),
                    "Impuestos USD": round(impuestos, 2),
                    "Utilidad bruta USD": resultado["utilidad_bruta"],
                    "Utilidad neta USD": resultado["utilidad_neta"],
                    "Margen neto %": resultado["margen_neto_pct"],
                }
                st.session_state.historico_margen.append(fila)
                st.success("Funcion ejecutada correctamente.")
            except ValueError as error:
                st.error(str(error))

    historico = st.session_state.historico_margen
    if historico:
        ultimo = historico[-1]
        col1, col2, col3 = st.columns(3)
        col1.metric("Utilidad bruta", f"USD {ultimo['Utilidad bruta USD']:,.2f}")
        col2.metric("Utilidad neta", f"USD {ultimo['Utilidad neta USD']:,.2f}")
        col3.metric("Margen neto", f"{ultimo['Margen neto %']:,.2f}%")
        st.subheader("Historico de resultados")
        st.dataframe(pd.DataFrame(historico), use_container_width=True, hide_index=True)
    else:
        st.info("Ejecute la funcion para iniciar el historico.")

    if st.button("Limpiar historico"):
        st.session_state.historico_margen = []
        st.rerun()


def ejercicio_4():
    st.title("Ejercicio 4 - Clase externa con CRUD Unificado")
    st.markdown(
        "Interfaz consolidada para administrar productos disponibles para exportación. "
        "Utiliza la clase `InventarioProducto` desde `libreria_clases_proyecto1.py`."
    )

    productos = st.session_state.productos_exportacion
    codigos = [p["Codigo"] for p in productos]
    
    # Determinar si estamos en modo edición
    editando_codigo = st.session_state.get("editando_codigo")
    
    # --- FORMULARIO DE REGISTRO / ACTUALIZACIÓN ---
    st.subheader("Registrar / Modificar Producto")
    
    # Variables por defecto
    val_codigo = ""
    val_nombre = ""
    val_costo = 0.0
    val_precio = 0.0
    val_stock = 0
    val_stock_min = 0
    
    # Si estamos editando, cargar la información del producto
    if editando_codigo and editando_codigo in codigos:
        prod_actual = next(p for p in productos if p["Codigo"] == editando_codigo)
        val_codigo = prod_actual["Codigo"]
        val_nombre = prod_actual["Producto"]
        val_costo = float(prod_actual["Costo unitario USD"])
        val_precio = float(prod_actual["Precio exportacion USD"])
        val_stock = int(prod_actual["Stock actual"])
        val_stock_min = int(prod_actual["Stock minimo"])

    # Definimos la lista de opciones basándonos en el Ejercicio 2
    lista_prendas = [
        "Camisas",
        "Tank",
        "T-Shirt Manga corta",
        "T-Shirt Manga larga",
        "T-shirt con estampado",
        "T-shirt con bordado",
        "T-shirt sublimado",
        "Short",
    ]
    
    # Calculamos el índice para que al "Modificar" se seleccione automáticamente el valor correcto
    index_prenda = lista_prendas.index(val_nombre) if val_nombre in lista_prendas else 0

    # Utilizamos un formulario para el ingreso de datos
    with st.form("form_crud_producto", clear_on_submit=False):
        col1, col2 = st.columns(2)
        # El código se deshabilita si estamos editando para mantener la integridad
        codigo = col1.text_input("Codigo", value=val_codigo, disabled=bool(editando_codigo), placeholder="Ej. PROD001")
        
        # Generamos un selectbox y le asignamos el nombre "Producto_Estilo"
        nombre = col2.selectbox("Producto_Estilo", lista_prendas, index=index_prenda)
        
        col3, col4 = st.columns(2)
        costo = col3.number_input("Costo unitario USD", min_value=0.0, step=1.0, value=val_costo)
        precio = col4.number_input("Precio exportacion USD", min_value=0.0, step=1.0, value=val_precio)
        
        col5, col6 = st.columns(2)
        stock_actual = col5.number_input("Stock actual", min_value=0, step=1, value=val_stock)
        stock_minimo = col6.number_input("Stock minimo", min_value=0, step=1, value=val_stock_min)
        
        # El botón cambia su texto según el contexto
        label_boton = "Actualizar producto" if editando_codigo else "Crear producto"
        guardar = st.form_submit_button(label_boton)

    if guardar:
        if not codigo.strip():
            st.error("Ingrese el código del producto.")
        else:
            codigo_limpio = codigo.strip().upper()
            try:
                # Se genera el nuevo registro usando la función que emplea la clase externa
                nuevo_registro = crear_registro_producto(
                    codigo_limpio, nombre, costo, precio, stock_actual, stock_minimo
                )
                
                if editando_codigo:
                    # Actualizar registro existente
                    indice = codigos.index(editando_codigo)
                    st.session_state.productos_exportacion[indice] = nuevo_registro
                    st.success("Producto actualizado correctamente.")
                    st.session_state["editando_codigo"] = None  # Salir de modo edición
                    st.rerun()
                else:
                    # Crear registro nuevo
                    if codigo_limpio in codigos:
                        st.error("Ya existe un producto con ese código.")
                    else:
                        st.session_state.productos_exportacion.append(nuevo_registro)
                        st.success("Producto creado correctamente.")
                        st.rerun()
            except ValueError as error:
                st.error(str(error))

    # Botón para cancelar la edición por si el usuario cambia de opinión
    if editando_codigo:
        if st.button("❌ Cancelar edición"):
            st.session_state["editando_codigo"] = None
            st.rerun()

    st.markdown("---")

    # --- RESUMEN DE DATOS ---
    st.subheader("Resumen de productos")
    mostrar_dataframe(
        st.session_state.productos_exportacion,
        "Aun no hay productos registrados.",
    )

    # --- ACCIONES DE MODIFICACIÓN Y ELIMINACIÓN ---
    if productos:
        st.markdown("### Acciones")
        # Estructuramos las columnas para alinear el selectbox y los botones
        col_sel, col_btn1, col_btn2 = st.columns([2, 1, 1])
        
        codigo_accion = col_sel.selectbox(
            "Seleccione un producto para modificar o eliminar:", 
            codigos, 
            key="accion_codigo"
        )
        
        with col_btn1:
            st.write("") # Espacios para alinear verticalmente con el selectbox
            st.write("")
            if st.button("✏️ Modificar", use_container_width=True):
                st.session_state["editando_codigo"] = codigo_accion
                st.rerun()
                
        with col_btn2:
            st.write("")
            st.write("")
            if st.button("🗑️ Eliminar", use_container_width=True):
                # Se filtra la lista para excluir el código seleccionado
                st.session_state.productos_exportacion = [
                    p for p in st.session_state.productos_exportacion if p["Codigo"] != codigo_accion
                ]
                # Si se elimina el producto que se estaba editando, se cancela la edición
                if st.session_state.get("editando_codigo") == codigo_accion:
                    st.session_state["editando_codigo"] = None
                st.success(f"Producto {codigo_accion} eliminado correctamente.")
                st.rerun()


def main():
    inicializar_estado()

    st.sidebar.title("Menu del proyecto")
    seccion = st.sidebar.selectbox(
        "Seleccione una seccion",
        ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"],
    )
    st.sidebar.markdown(
        f"""
        <div class="active-section-box">
            <span>Seccion activa</span>
            <strong>{seccion}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if seccion == "Home":
        pagina_home()
    elif seccion == "Ejercicio 1":
        ejercicio_1()
    elif seccion == "Ejercicio 2":
        ejercicio_2()
    elif seccion == "Ejercicio 3":
        ejercicio_3()
    elif seccion == "Ejercicio 4":
        ejercicio_4()


if __name__ == "__main__":
    main()
