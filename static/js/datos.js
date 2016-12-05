$(document).ready(function() {
	$("#Gencurp").click(function()
	{
		var array_meses=["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"];
		var fecha=($("#fNacer").val()).split("-"); //["año","mes","dia"]
		var indice=eval(fecha[1]-1);//numero de mes
		var mes=array_meses[indice];

		var datos={
			nombre:$("#nombres").val(),
			paterno:$("#paterno").val(),
			materno:$("#materno").val(),
			anio:fecha[0],
			mes:mes,
			dia:fecha[2],
			entidad:$("#entidad").val(),
			sexo:$("#sexo").val(),
			
			direccion:$("#direccion").val(),
			correo:$("#correo").val(),
			telefono:$("#telefono").val(),
			nControl:$("#cControl").val(),
			escuela:$("#escuela").val(),
			semestre:$("#semestre").val(),
			carrera:$("#carrera").val()
			};
			console.log(datos);

			$.ajax({  // envia al servidor 
                    url:'http://localhost:3000/datos',
                    data:datos,
                    type:'post',
                    success:function (respuesta) {
                        console.log(respuesta);
                    }
        	});

	});
});