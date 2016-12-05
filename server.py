from flask import Flask, render_template, jsonify, request
import string
import random
import pdfkit


app=Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/datos', methods=["GET","POST"])
def add_datos():
	
	datos=request.form #recibe los datos en formato json
	##########################################
	curp=""
	nombrepila=""
	mesesnombres=["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
	mesesnum=["01","02","03","04","05","06","07","08","09","10","11","12"]
	vocales=['A','E','I','O','U']
	consonantes=['B','C','D','F','G','H','J','K','L','M','N','Ñ','P','Q','R','S','T','V','W','X','Y','Z']
	mesfinal=""
	listanombres=((request.form['nombre']).upper()).split(" ")#separa los nombres en un array
	paterno=(request.form['paterno']).upper()
	materno=(request.form['materno']).upper()
	anio=(request.form['anio']).upper()
	mes=(request.form['mes'])
	dia=(request.form['dia']).upper()
	entidad=(request.form['entidad']).upper()
	s=(request.form['sexo']).upper()
	#################################################3
	curp +=paterno[0:1]
	#ENCONTRAR PRIMERA VOCAL DEL PRIMER APELLIDO
	j=1
	vocal=""
	primervocal=False
	while j<len(paterno) and primervocal==False:
		vocal = paterno[j]
		for v in vocales:
			if v == vocal:
				primervocal=True
		j+=1
	curp += vocal

    #ADJUNTAMOS LA INICIAL DEL SEGUNDO APELLIDO
	curp += materno[0:1]

    #ADJUNTAMOS LA INICIAL DEL NOMBRE
     #CONDICIONES PARTICULARES PARA SABER QUE NOMBRE TOMAR
	i=0
	bandera=False
	while i<len(listanombres) and bandera==False:
        #Si el unico nombre es JOSE
		if listanombres[i]=="JOSE" and ((listanombres[i+1]=="" or listanombres[i+1]==None) and (listanombres[i+2]=="" or listanombres[i+2]==None) and (listanombres[i+3]=="" or listanombres[i+3]==None)):
			nombrepila=listanombres[i]
        #Si el primer nombres es Jose y hay mas nombres, que tome el segundo
		elif listanombres[i]=="JOSE" and listanombres[i+1]!="":
			nombrepila = listanombres[i+1]
        #Analizar si MARIA es el unico nombre si es asi, se toma el nombre de Maria
		elif listanombres[i]=="MARIA" and ((listanombres[i+1]=="" or listanombres[i+1]==None) and (listanombres[i+2]=="" or listanombres[i+2]==None) and (listanombres[i+3]=="" or listanombres[i+3]==None)):
			nombrepila=listanombres[i]
        #Analizar si en el nombre se encuentra el nombre de MARIA DE LOS, si es asi, toma el cuarto nombre
		elif listanombres[i]=="MARIA" and listanombres[i+1]=="DE" and listanombres[i+2]=="LOS":
			nombrepila = listanombres[i+3]
        #Analizar si en el nombre se encuentra el nombre de MARIA DE LA, si es asi, toma el cuarto nombre
		elif listanombres[i]=="MARIA" and listanombres[i+1]=="DE" and listanombres[i+2]=="LA":
			nombrepila = listanombres[i+3]
        #Analizar si en el nombre aparece el nombre de MARIA DEL entonces toma el tercer nombre
		elif listanombres[i]=="MARIA" and listanombres[i+1]=="DEL":
			nombrepila = listanombres[i+2]
        #Analizar si en el nombre aparece MARIA DE, entonces toma el tercer nombre, siempre y cuando en este no aparezcan los nombres LA, LOS
		elif listanombres[i]=="MARIA" and listanombres[i+1]=="DE" and listanombres[i+2]!="LA" and listanombres[i+2]!="LOS":
			nombrepila = listanombres[i+3]
        #Analizar si tiene mas de 2 nombres y el primero es MARIA, entonces toma el segundo
		elif listanombres[i]=="MARIA" and listanombres[i+1]=="DE" and listanombres[i+2]!="DEL":
			nombrepila = listanombres[i+1]
		else:
			bandera=True
		i+=1

	if bandera:
		nombrepila = listanombres[0]
   	#ADJUNTAR NOMBRE DE PILA AL CURP UNA VEZ ANALIZADAS LAS CONDICIONES
	curp += nombrepila[0:1]

	#ADJUNTAMOS el AÑO, MES ,DIA DE NACIMIENTO
    #----------------------AÑO--------------
	curp += anio[2:]
    #--------------------MES-----------------------------
	pos=0
	for m in range(0,len(mesesnombres)):
		print(mesesnombres[m])
		print(mes)
		if mesesnombres[m]==mes:
			pos=m	
	mesfinal=mesesnum[pos]
	curp += mesfinal
    #---------------------DIA----------------------
	curp += dia

	#ADJUNTAMOS EL SEXO DE LA PERSONA , H -HOMBRE, M-MUJER

	curp += s

	#ADJUTAMOS  LA CLAVE DELA ENTIDAD FEDERATIVA DE nacimiento
	estado={
		"AGUASCALIENTES":"AS","M":"NA", "BAJA CALIFORNIA":"BC", "BAJA CALIFORNIA SUR":"BS","CAMPECHE":"CC",
		"COAHUILA DE ZARAGOZA":"CL","COLIMA":"CM","CHIAPAS":"CS","CHIHUAHUA":"CH","DISTRITO FEDERAL":"DF",
		"DURANGO":"DG","GUANAJUATO":"GT","GUERRERO":"GR","HIDALGO":"HG","JALISCO":"JC","ESTADO DE MEXICO":"MC",
		"MICHOACAN DE OCAMPO":"MN","MORELOS":"MS","NAYARIT":"NT","NUEVO LEON":"NL","OAXACA":"OC","PUEBLA":"PL",
		"QUERETARO DE ARTEAGA":"QT","QUINTANA ROO":"QR","SAN LUIS POTOSI":"PT","SINALOA":"SL","SONORA":"SR",
		"TABASCO":"TC","TAMAULIPAS":"TS","TLAXCALA":"TL","VERAZCRUZ":"VZ","YUCATAN":"YN","ZACATECAS":"ZS",
		"EXTRANEJERO":"NE"
	}
	curp += estado[entidad]

    #Primera consonante interna (no inicial) del primer apellido.
	j=1
	primerconsonante=False
	consonante=""
	while j<len(paterno) and primerconsonante==False:
		consonante = paterno[j]
		for c in consonantes:
			if c == consonante:
				primerconsonante=True
		j+=1
    #if consonante=='Ñ':
    #    curp += 'X'
    #else:
	curp += consonante

	#Primera consonante interna (no inicial) del segundo apellido.
	j=1
	segunda_consonante=False
	consonante2=""
	while j<len(materno) and segunda_consonante==False:
		consonante2 = materno[j]
		for c in consonantes:
			if c == consonante2:
				segunda_consonante=True
		j+=1
    #if consonante2=='Ñ':
    #    curp += 'X'
    #else:
	curp += consonante2

    #Primer consonante no inicial del nombre de pila
	j=1
	consonantenombre=False
	consonantenom=""
	while j<len(nombrepila) and consonantenombre==False:
		consonantenom = nombrepila[j]
		for c in consonantes:
			if c == consonantenom:
				consonantenombre=True
		j+=1
    #if consonantenom=='Ñ':
    #    curp += 'X'
    #else:
	curp += consonantenom

    #ULTIMOS DOS DIGITOS dígito del 0-9 para fechas de nacimiento hasta el año 1999 y A-Z para fechas de nacimiento a partir del 2000.
    #------Primer digito al azar--------
	def id_generator(size=1, chars=string.ascii_uppercase):#+ string.digits):
		return ''.join(random.choice(chars) for _ in range(size))

	if(int(anio)<2000):
		digito1=random.randrange(10)
	else:
		digito1=id_generator(1)

	curp +=str(digito1)

    #------Segundo digito al azar--------
	digito2=random.randrange(10)
	curp += str(digito2)

    #VERIFICAR AL FINAL SI EXISTE UN A Ñ EN EL CURP SI ES ASI CAMBIARLA
	curptem=list(curp)
	for i in range(0,len(curptem)):
		if curptem[i]=="Ñ":
			curp[i:i+1]="X"
    #SE NECESITA HACER CONVERTIR CURP DE CADENA A LISTA ASÍ SE ELIMINARIAN LAS CONDICIONES DESPUES DE ENCONTRAR CADA CONSONANTE

    #VERIFICAR LO DE LAS PALABRAS ALTISONANTES
	inconvenientes = ['BACA', 'LOCO', 'BUEI', 'BUEY', 'MAME', 'CACA', 'MAMO',
		'CACO', 'MEAR', 'CAGA', 'MEAS', 'CAGO', 'MEON', 'CAKA', 'MIAR', 'CAKO', 'MION',
		'COGE', 'MOCO', 'COGI', 'MOKO', 'COJA', 'MULA', 'COJE', 'MULO', 'COJI', 'NACA',
		'COJO', 'NACO', 'COLA', 'PEDA', 'CULO', 'PEDO', 'FALO', 'PENE', 'FETO', 'PIPI',
		'GETA', 'PITO', 'GUEI', 'POPO', 'GUEY', 'PUTA', 'JETA', 'PUTO', 'JOTO', 'QULO',
		'KACA', 'RATA', 'KACO', 'ROBA', 'KAGA', 'ROBE', 'KAGO', 'ROBO', 'KAKA', 'RUIN',
		'KAKO', 'SENO', 'KOGE', 'TETA', 'KOGI', 'VACA', 'KOJA', 'VAGA', 'KOJE', 'VAGO',
		'KOJI', 'VAKA', 'KOJO', 'VUEI', 'KOLA', 'VUEY', 'KULO', 'WUEI', 'LILO', 'WUEY',
		'LOCA']
	if curp[:4] in inconvenientes:
		curp=curp[:1] + 'X' + curp[2:]

    #ENVIO DE CURP AL TEXTINPUT
	#display.text=curp
	print(curp)
	return jsonify({'status': True}), 200

@app.route('/camara')
def camara():
	return render_template('camara.html')

@app.route('/img', methods=["GET","POST"])
def img():
	global src
	src = request.form['src']# sacamos la variable que mando el cliente
	return jsonify({'status': True}), 200 #retornamosun json para confirmar

app.run(debug=True, port=8000)
