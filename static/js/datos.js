$(document).ready(function() {
	$("#Gencurp").click(function()
	{
		var datos={
			nombre:$("#nombres").val(),
			paterno:$("#paterno").val(),
			materno:$("#materno").val(),
			fNacer:$("#fNacer").val(),
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