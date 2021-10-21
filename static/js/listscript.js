let tabla = document.getElementById("tabla");

/*let data = [
    {
        descrip: "Odontología",
        paciente:"Jose P.",
        id: "12345678", 
        doctor: "Julian R",
        idd: "12345678",
        fecha:"2021-10-13 - 12:00",
        coment: "comentario"
    },
    {
        descrip: "Pediatría",
        paciente:"Angel D.", 
        id: "12345678",
        doctor: "Daniela Z",
        idd: "12345678",
        fecha:"2021-10-28 - 13:00",
        coment: "comentario"
    }
];*/

/*
function add_form()
{
    document.getElementById("dark").style.background = "rgba(0, 0, 0, .7)";
    document.getElementById("dark").style.visibility = "visible";
    console.log("add");
    let add = document.getElementById("w-edit");
    let out = `<div style="width: 62rem; margin: auto; text-align: right;">
                    <img id="close" src="/static/img/close-icon.png" alt="" style="width: 23px; cursor: pointer;">
               </div">
               <div style="width: 62rem; margin: auto;">
                    <div style="text-align:left;background-color:white;padding:1rem;background-clip: border-box; border: 1px solid rgba(0,0,0,.125); border-radius: .25rem;">
                        <div id="row">
                            <label>Datos Medico</label>
                        </div>
                        <div id="row">
                            <div id="col" style="width: 22%;float: left;padding: 1rem;">
                                <div class="form-group">
                                    <label for="especialidad">Especialidad </label>
                                    <select id="especialidad"class="form-control" name"especialidad">
	                                    <option>Odontología</option>
	                                    <option>Pediatría</option>
	                                    <option>General</option>
	                                </select>
                                </div>
                            </div>
                            <div id="col" style="width: 22%;float: left;padding: 1rem;">
                                <div class="form-group">
                                    <label for="medico">Medico </label>
                                    <select id="medico"class="form-control" name"medico">
	                                    <option>Daniel R.</option>
	                                    <option>Carlos P.</option>
	                                    <option>Daniela G.</option>
	                                </select>
                                </div>
                            </div>
                            <div id="col" style="width: 22%;float: left;padding: 1rem;margin-right: 14rem;">
                                <div class="form-group">
                                    <label for="fecha">Fecha </label>
                                    <input type="date" id="date" name"fecha">
                                </div>
                            </div>
                        </div>
                        <div id="row" style="width:30%;">
                            <div id="col" style="padding:1rem;">
                                <div class="form-group">
                                    <label for="hora">Hora </label>
                                    <select id="hora" class="form-control" name"hora">
	                                    <option>10:00</option>
	                                    <option>12:30</option>
	                                    <option>16:00</option>
	                                </select>
                                </div>
                            </div>
                        </div>
                        <div id="row">
                            <label>Datos Paciente</label>
                        </div>
                        <div id="row">
                            <div id="col" style="width: 22%;float: left;padding: 1rem;">
                                <div class="form-group">
                                    <label for="tipoid">Tipo ID </label>
                                    <select id="tipoid"class="form-control" name"tipoid">
	                                    <option>C.C</option>
	                                    <option>T.I</option>
	                                    <option>T.E</option>
	                                </select>
                                </div>
                            </div>
                            <div id="col" style="width: 33%;float: left;padding: 1rem;">
                                <div class="form-group">
                                    <label for="id">No ID </label>
                                    <input id="id" type="text" name="id">
                                </div>
                            </div>
                            <div id="col" style="width: 33%;float: left;padding: 1rem;margin-right: 2rem;">    
                                <div class="form-group">
                                    <label for="nombre">Nombre </label>
                                    <input id="nombre"type="text" name="nombre">
                                </div>
                            </div>
                        </div>
                        <div id="row" style="float:left;">
                            <div id="col" style="width: 33%;float: left;padding: 1rem;">
                                <div class="form-group">
                                    <label for="apellido">Apellido</label>
                                    <input id="apellido"type="text" name="apellido">
                                </div>
                            </div>
                            <div id="col" style="width: 33%;float: left;padding: 1rem;margin-right: 2rem;">
                                <div class="form-group">
                                    <label for="email">Correo electrónico</label>
                                    <input id="email" type="email" name="email">
                                </div>
                            </div>
                        </div>
                        <div id="row">
                            <div id="col">
                                <div class="form-group">
                                    <label for="comentario">Comentarios </label>
                                    <textarea id="comentario" class="form-control" rows="3" name="comentario">
                                    </textarea>
                                </div>
                            </div>
                        </div>
                        <div id="row" style="width:30%;margin:auto;">
                            <div id="col">    
                                <button id="add_btn" class="btn btn-default form-control">Guardar</button>
                            </div>
                        </div>
                    </div>
               </div>`;
    add.innerHTML = out;
    document.getElementById("close").addEventListener("click", ()=>close_());
    document.getElementById("add_btn").addEventListener("click", ()=>add_data());
}*/
function add_data()
{
    let especialidad = document.getElementById("especialidad").value;
    let medico = document.getElementById("medico").value;
    let date = document.getElementById("date").value;
    let hora = document.getElementById("hora").value;
    let idp = document.getElementById("id").value;
    let nombre = document.getElementById("nombre").value;
    let apellido = document.getElementById("apellido").value;
    let email = document.getElementById("email").value;
    let comentario = document.getElementById("comentario").value;

    if((idp == "") && (nombre=="") && (apellido=="") &&(email=="")&&(date==""))
    {
        alert("Formulario incompleto");
    }
    else
    {
        let tmp = {
            descrip: especialidad,
            paciente: nombre+" "+apellido,
            id: idp, 
            doctor: medico,
            idd: "12345678",
            fecha: date+" - "+hora,
            coment: comentario
        }
        data.push(tmp);
        alert("datos guardados");
        close_();
        mk_table();
    }
}
function edit(index)
{ 
    document.getElementById("dark").style.background = "rgba(0, 0, 0, .7)";
    document.getElementById("dark").style.visibility = "visible";
    console.log("edit");
    wedit_(index);
}

function delete_form(index)
{
    document.getElementById("dark").style.background = "rgba(0, 0, 0, .7)";
    document.getElementById("dark").style.visibility = "visible";
    console.log("delete");
    let del = document.getElementById("w-edit");
    let out = `<div style="width: 21rem; margin: auto; text-align: right;">
                    <img id="close" src="/static/img/close-icon.png" alt="" style="width: 23px; cursor: pointer;">
               </div">
               <div style="width: 21rem; margin: auto;">
                    <div style="text-align:left;background-color:white;padding:1rem;background-clip: border-box; border: 1px solid rgba(0,0,0,.125); border-radius: .25rem;">
                        <div id="row">
                            <label>Desea eliminar la Cita: #${index+1}</label>
                        </div>
                        <div id="row">
                            <div id="col">    
                                <button id="delete_btn" class="btn btn-default form-control">Eliminar</button>
                            </div>
                        </div>
                    </div>
                </div>`;
    del.innerHTML = out;
    document.getElementById("close").addEventListener("click", ()=>close_());
    document.getElementById("delete_btn").addEventListener("click", ()=>delete_(index));
}

function delete_(index)
{
    console.log("index:"+index);
    data.splice(index, 1);
    alert("datos eliminados");
    close_();
    mk_table();
}
function close_()
{
    document.getElementById("w-edit").innerHTML = "";
    //content.style.pointerEvents = "auto";
    document.getElementById("dark").style.background = "rgba(0, 0, 0, 0)";
    document.getElementById("dark").style.visibility = "collapse";
    console.log("close");    
}

function wedit_(index)
{
    $.ajax({
        type:'GET',
        url:'/wedit',
        data:{jsdata: index},
        success:function(response)
        {
            document.getElementById("w-edit").innerHTML = response;
        }
    });
}

function mk_table()
{
    document.getElementById("add").addEventListener("click" ,function(e)
            {
                document.getElementById("dark").style.background = "rgba(0, 0, 0, .7)";
                document.getElementById("dark").style.visibility = "visible";
                e.preventDefault();
                $.ajax({
                    type:'GET',
                    url:'/citasForm',
                    success:function(response)
                    {
                        document.getElementById("w-edit").innerHTML = response;
                        document.getElementById("close").addEventListener("click", ()=>close_());
                    }
                });
    });
        

}
document.addEventListener("load", mk_table());
