const btnDelete = document.querySelectorAll('.btn-delete')//devuelve una lista de nodos con todos los botones de esa clase
if (btnDelete){
    const btnArray = Array.from(btnDelete) //lo transforma en un array
    btnArray.array.forEach((btn) => {//a cada botón
        btn.addEventListener('click', (e) =>{
            if(!confirm('Are you sure you want to delete if?')){
                e.preventDefault(); //anula el listener
            } //sino no hace nada y se ejecuya la acción del botón
        });
    });
}