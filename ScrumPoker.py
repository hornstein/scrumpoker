#! /usr/bin/env python

import os

from flask import Flask
from flask import request, Response, jsonify
#from flask import render_template, send_from_directory


import requests

mydict={}
mydict2={}
revealScores=False

app = Flask(__name__)


@app.route('/')
def start():
    global revealScores
    revealScores=False
    return """
<html>
	<head>
		<title>Scrum Poker</title>
		<meta charset="UTF-8">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>

		<script>
			$(document).ready(function(){


				$("#reset").click(function(){
					$.get('reset', function(data, status){
						console.log(`${data}`)
					});
				})

				$("#reveal").click(function(){
					$.get('reveal', function(data, status){
						console.log(`${data}`)
					});
				})

				$(".button").click(function(){
					$.getJSON( "vote", {name: $('#name').val(), score: $(this).val()}, function( data ) {
					});
				})

				function poll(){
					$.getJSON( "getvotes", function( data ) {
						$("#votes").html('');
						$.each( data, function( key, val ) {
							$("#votes").append( key + ': '  + val + '<br>' );
						});
					});
				}

				setInterval(poll, 2000);
			})

		</script>
		
	</head>
	<body>

		<div class="frame">

			<div class="topnav">
				<h1>Scrum Poker</h1>
			</div>
			
			<div style="padding-left:16px">
				<br>
				Enter your name: <input type="text" id="name"><br>
				<br>
				<hr>
				<br>
				<h2>Your score</h2>
				<button value="1" class="button">1</button>
				<button value="2" class="button">2</button>
				<button value="3" class="button">3</button>
				<button value="5" class="button">5</button>
				<button value="8" class="button">8</button>
				<button value="13" class="button">13</button>
				<button value="20" class="button">20</button>
				<button value="0" class="button">?</button>
				<button value="99" class="button">Coffee</button>
				<br>
				<hr>
				<br>
				<button id="reveal">Reveal</button>
				<button id="reset">Reset</button>
				<br>
				<hr>
				<br>
				<h2>Votes</h2>
				<div id="votes">
				</div>

			</div>
		</div>
	</body>
</html>

        """
    # return render_template('index.html', name='Scrum poker')


@app.route('/reset')
def reset():
    global mydict, mydict2, revealScores
    mydict={}
    mydict2={}
    revealScores=False
    return 200


@app.route('/reveal')
def reveal():
    global revealScores
    revealScores=True
    return 200


@app.route('/vote')
def vote():
    global mydict, mydict2
    name = request.args.get('name')
    score = int(request.args.get('score'))
    mydict.update({name: score})
    mydict2.update({name: 0})
    return jsonify(mydict)


@app.route('/getvotes')
def getvotes():
    global mydict, mydict2, revealScores
    if revealScores:
        return jsonify(mydict)
    return jsonify(mydict2)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)