let tabla = document.getElementById("tabla");

let data = [
    {
        descrip: "Odontología",
        paciente:"Jose P.",
        id: "12345678", 
        doctor: "Julian R",
        idd: "12345678",
        fecha:"12/01/21 - 13:30"
    },
    {
        descrip: "Pediatría",
        paciente:"Angel D.", 
        id: "12345678",
        doctor: "Daniela Z",
        idd: "12345678",
        fecha:"28/01/21 - 10:00"
    }
];

function edit(index)
{ 
    document.getElementById("dark").style.background = "rgba(0, 0, 0, .7)";
    document.getElementById("dark").style.visibility = "visible";
    console.log("edit");
    wedit_(index);
    document.getElementById("close").addEventListener("click", ()=>close_());
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
    let wedit = document.getElementById("w-edit");
    let out = `<div style="width: 32rem; margin: auto; text-align: right;">
                    <img id="close" src="static/img/close-icon.png" alt="" style="width: 23px; cursor: pointer;">
                    </div>
                    <div style="width: 32rem; margin: auto;">
                        <div class="card"style="padding:1rem;position: relative; display: flex; flex-direction: row;min-width: 0;word-wrap: break-word;background-color: #fff;background-clip: border-box;border: 1px solid rgba(0,0,0,.125);border-radius: .25rem;">
                        <div style="padding: 1rem; background-clip: border-box; border: 1px solid rgba(0,0,0,.125); border-radius: .25rem; ">
                            <p><strong>Detalle de cita #${index+1}</strong></p>
                            <p>Fecha de cita: ${data[index].fecha}</p>
                            <p>Paciente: ${data[index].paciente}</p>
                            <p>ID: ${data[index].id}</p>
                            <p>Doctor: ${data[index].doctor}</p>
                            <p>ID: ${data[index].idd}</p>
                            <p>Especialidad: ${data[index].descrip}</p>
                            <br>
                            <div style="background-clip: border-box;
                                border: 1px solid rgba(0,0,0,.125);
                                border-radius: .25rem; padding: 0.5rem;"><p>comentarios</p>
                            </div>
                        </div>
                        <div style="padding: 1rem;"> 
                            <div style="background-clip: border-box;
                                    border: 1px solid rgba(0,0,0,.125);
                                    border-radius: .25rem; padding: 1rem;">
                                    <img src="static/img/user-logo.png" width="96px">
                                    <p style="text-align: center;">${data[index].paciente}</p>
                            </div>
                            <div style="background-clip: border-box;
                                    border: 1px solid rgba(0,0,0,.125);
                                    border-radius: .25rem; padding: 1rem; margin-top: 2rem;">
                                    <img src="static/img/doctor-logo.png" width="96px">
                                    <p style="text-align: center;">${data[index].doctor}</p>
                            </div>
                        </div>
                    </div>
                </div>`;
    wedit.innerHTML = out;
}

function mk_table()
{
    let out = `<div style="color:#777;padding:1rem;"><p><strong>Listado de citas</strong></p></div>
    <div class="table-responsive" style="background-clip: border-box; border: 1px solid rgba(0,0,0,.125); border-radius: .25rem; padding: 1rem;">
    <table class="table">
        <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Descripción</th>
            <th scope="col">Paciente</th>
            <th scope="col">Doctor</th>
            <th scope="col">Fecha/Hora</th>
            <th></th>
        </tr>
        </thead>
        <tbody>`
    data.forEach((item, index) =>{out += `<tr>
                                            <th scope="row">${index+1}</th>
                                            <td>${item.descrip}</td>
                                            <td>${item.paciente}</td>
                                            <td>${item.doctor}</td>
                                            <td>${item.fecha}</td>
                                            <td>
                                                <img id="edit${index}"  onclick="edit(${index})" src="static/img/view.png" alt="" style="width: 33px; margin-right: 12px; cursor: pointer;">
                                                <img id="delete${index}" src="static/img/deleted-logo.png" alt="" style="width: 23px; cursor: pointer;">
                                            </td>
                                        </tr>`
                                    });
    out += `</tbody>
            </table>
            <div><img id="add" src="static/img/add-logo.png" alt="" style="width:30px; cursor:pointer;"></div>
            </div>`
    tabla.innerHTML = out;
}
document.addEventListener("load", mk_table());