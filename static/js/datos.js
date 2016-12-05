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
			año:fecha[0],
			mes:mes,
			dia:fecha[2],
			direccion:$("#direccion").val(),
			entidad:$("#entidad").val(),
			sexo:$("#sexo").val(),
			};
			console.log(datos);
		// $.get('http://192.168.43.67:8080/setDatos',datos,function(datos,status)
		// 	{
		// 		alert(status);
		// 	});	
	});
});