var path = require('path')
var express = require('express')
var fs = require('fs')


var app = express()

var port = process.env.PORT || 3000

app.use(express.static('public'))

app.use('/images', express.static('./images'))
app.use(express.json())

app.get("/", function(req, res) {
    res.status(200).sendFile(path.join(__dirname, 'public/index.html'))
})

app.get("/settings", function(req, res) {
    res.status(200).sendFile(path.join(__dirname, 'public/settings.html'))
})

app.get("/locations", function(req, res) {
    res.status(200).sendFile(path.join(__dirname, 'public/locations.html'))
})

app.get("/information", function(req, res) {
    res.status(200).sendFile(path.join(__dirname, 'public/information.html'))
})

app.listen(port, function() {
    console.log("Listening on port", port)
})
