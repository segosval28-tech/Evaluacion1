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
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .hero-box {
            padding: 24px;
            border-radius: 8px;
            background: linear-gradient(135deg, #0f3d5e, #047857);
            color: white;
            margin-bottom: 18px;
        }
        .hero-box h1 {
            color: white;
            margin-bottom: 8px;
        }
        .hero-box p {
            color: rgba(255,255,255,0.88);
            margin-bottom: 0;
        }
        .info-box {
            padding: 16px;
            border: 1px solid #d7dee8;
            border-radius: 8px;
            background: #f8fafc;
        }
        .small-muted {
            color: #64748b;
            font-size: 0.92rem;
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
        concepto = col1.text_input("Concepto del movimiento", placeholder="Ej. Flete internacional")
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
        if not concepto.strip():
            st.error("Ingrese un concepto para registrar el movimiento.")
        elif valor <= 0:
            st.error("El valor debe ser mayor que cero.")
        else:
            st.session_state.movimientos_exportacion.append(
                {
                    "Concepto": concepto.strip(),
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
        producto = col1.text_input("Producto", placeholder="Ej. Prendas de vestir")
        cliente = col2.text_input("Cliente extranjero", placeholder="Ej. Cliente USA")
        pais = col3.text_input("Pais destino", placeholder="Ej. Estados Unidos")

        col4, col5, col6 = st.columns(3)
        via = col4.selectbox("Via de transporte", ["Maritimo", "Aereo"])
        incoterm = col5.selectbox("Incoterm", ["FOB", "CFR", "CIF", "DAP", "DDP", "EXW"])
        cantidad = col6.number_input("Cantidad", min_value=1, step=1)

        precio = st.number_input("Precio unitario USD", min_value=0.0, step=1.0, format="%.2f")
        agregar = st.form_submit_button("Agregar embarque")

    if agregar:
        if not producto.strip() or not cliente.strip() or not pais.strip():
            st.error("Complete producto, cliente y pais destino.")
        elif precio <= 0:
            st.error("El precio unitario debe ser mayor que cero.")
        else:
            total = cantidad * precio
            st.session_state.embarques_exportacion.append(
                {
                    "Producto": producto.strip(),
                    "Cliente": cliente.strip(),
                    "Pais destino": pais.strip(),
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
        operacion = st.text_input("Operacion o referencia", placeholder="Ej. EXP-2026-001")
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
    st.title("Ejercicio 4 - Clase externa con CRUD")
    st.markdown(
        "Uso de la clase `InventarioProducto` desde `libreria_clases_proyecto1.py` "
        "para administrar productos disponibles para exportacion."
    )

    tab_crear, tab_leer, tab_actualizar, tab_eliminar = st.tabs(
        ["Crear", "Leer", "Actualizar", "Eliminar"]
    )

    with tab_crear:
        with st.form("form_crear_producto", clear_on_submit=True):
            col1, col2 = st.columns(2)
            codigo = col1.text_input("Codigo", placeholder="Ej. PROD001")
            nombre = col2.text_input("Producto", placeholder="Ej. Polo algodon")
            col3, col4 = st.columns(2)
            costo = col3.number_input("Costo unitario USD", min_value=0.0, step=1.0, key="crear_costo")
            precio = col4.number_input("Precio exportacion USD", min_value=0.0, step=1.0, key="crear_precio")
            col5, col6 = st.columns(2)
            stock_actual = col5.number_input("Stock actual", min_value=0, step=1, key="crear_stock")
            stock_minimo = col6.number_input("Stock minimo", min_value=0, step=1, key="crear_stock_min")
            crear = st.form_submit_button("Crear producto")

        if crear:
            codigos = [p["Codigo"] for p in st.session_state.productos_exportacion]
            if not codigo.strip() or not nombre.strip():
                st.error("Ingrese codigo y nombre del producto.")
            elif codigo.strip().upper() in codigos:
                st.error("Ya existe un producto con ese codigo.")
            else:
                try:
                    registro = crear_registro_producto(
                        codigo, nombre, costo, precio, stock_actual, stock_minimo
                    )
                    st.session_state.productos_exportacion.append(registro)
                    st.success("Producto creado correctamente.")
                except ValueError as error:
                    st.error(str(error))

    with tab_leer:
        mostrar_dataframe(
            st.session_state.productos_exportacion,
            "Aun no hay productos registrados.",
        )

    with tab_actualizar:
        productos = st.session_state.productos_exportacion
        if not productos:
            st.info("Primero cree un producto para poder actualizarlo.")
        else:
            codigos = [p["Codigo"] for p in productos]
            codigo_sel = st.selectbox("Seleccione producto", codigos, key="actualizar_codigo")
            actual = next(p for p in productos if p["Codigo"] == codigo_sel)

            with st.form("form_actualizar_producto"):
                nombre = st.text_input("Producto", value=actual["Producto"])
                col1, col2 = st.columns(2)
                costo = col1.number_input(
                    "Costo unitario USD",
                    min_value=0.0,
                    step=1.0,
                    value=float(actual["Costo unitario USD"]),
                    key="actualizar_costo",
                )
                precio = col2.number_input(
                    "Precio exportacion USD",
                    min_value=0.0,
                    step=1.0,
                    value=float(actual["Precio exportacion USD"]),
                    key="actualizar_precio",
                )
                col3, col4 = st.columns(2)
                stock_actual = col3.number_input(
                    "Stock actual",
                    min_value=0,
                    step=1,
                    value=int(actual["Stock actual"]),
                    key="actualizar_stock",
                )
                stock_minimo = col4.number_input(
                    "Stock minimo",
                    min_value=0,
                    step=1,
                    value=int(actual["Stock minimo"]),
                    key="actualizar_stock_min",
                )
                actualizar = st.form_submit_button("Actualizar producto")

            if actualizar:
                if not nombre.strip():
                    st.error("El nombre del producto no puede quedar vacio.")
                else:
                    try:
                        nuevo = crear_registro_producto(
                            codigo_sel, nombre, costo, precio, stock_actual, stock_minimo
                        )
                        indice = codigos.index(codigo_sel)
                        st.session_state.productos_exportacion[indice] = nuevo
                        st.success("Producto actualizado correctamente.")
                    except ValueError as error:
                        st.error(str(error))

    with tab_eliminar:
        productos = st.session_state.productos_exportacion
        if not productos:
            st.info("No hay productos para eliminar.")
        else:
            codigos = [p["Codigo"] for p in productos]
            codigo_sel = st.selectbox("Producto a eliminar", codigos, key="eliminar_codigo")
            st.warning("Esta accion elimina el registro solo de la sesion actual.")
            if st.button("Eliminar producto"):
                st.session_state.productos_exportacion = [
                    p for p in productos if p["Codigo"] != codigo_sel
                ]
                st.success("Producto eliminado correctamente.")
                st.rerun()


def main():
    inicializar_estado()

    st.sidebar.title("Menu del proyecto")
    seccion = st.sidebar.selectbox(
        "Seleccione una seccion",
        ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"],
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
