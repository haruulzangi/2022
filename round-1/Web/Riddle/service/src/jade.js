//Same for all javascritp template tengines
const express = require('express')
var bodyParser = require('body-parser');
const app = express()
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));
//Dependent of Templating engine
var jade = require('jade');
const port = 5069


function getHTML(input){
    var template =`
doctype
html
head
    title= 'Hello Gotham'
    link(href='/style.css', rel='stylesheet')
body
    form(action='/' method='post')
        label(for='name')
            input#name.form-control(type='text', placeholder='', class='input-search', name='name')
            br
            button.btn.btn-primary(type='submit', class='button-60') Riddle
    p Guess what `+input+`
    br
    img.image(src='/' + 'riddler.jpg', width='800', heigth='600' )`
    

    var fn = jade.compile(template);
    var html = fn({name:'Riddler'});
    console.log(input)
    console.log(html);
    return html;
}


app.post('/', (request, response) => {
    var input = request.param('name', "")
    var html = getHTML(input)
    response.send(html);
})


app.get('/', (request, response) => {
    var html = getHTML("")
    response.send(html)
  })


app.listen(port, (err) => {
if (err) {
    
    return console.log('something bad happened', err)
}

console.log(`server is listening on ${port}`)
})

