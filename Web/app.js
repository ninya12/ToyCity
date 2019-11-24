var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

var app = express();

app.io = require('socket.io')();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname + '/public/')));

app.use('/', indexRouter);
app.use('/users', usersRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

var net = require('net');
var image = '';
var sendData = 'NSND';
var imageBus = '';
var sendDataBus = 'NS';
var server = net.createServer(function(client) {
  console.log('Client connection: ');
  console.log('   local = %s:%s', client.localAddress, client.localPort);
  console.log('   remote = %s:%s', client.remoteAddress, client.remotePort);
  client.setTimeout(1500);
  client.on('data', function(data) {
    if(data.toString().substr(0,4) == "/9j/"){
      image = '';
    }
    image += data.toString();
    var sendLength = '';
    if(sendData.length > 0){
      if(sendData.length < 10){
        sendLength = '0' + sendData.length
      }
      sendData = sendLength + sendData;
      writeData(client, sendData);
      console.log("send data to pi " + sendData + " " + sendData.length)
      sendData = "";
    }
  });
  client.on('end', function() {
    console.log('Client disconnected');
    server.getConnections(function(err, count){
      console.log('Remaining Connections: ' + count);
    });
  });
  client.on('error', function(err) {
    console.log('Socket Error: ', JSON.stringify(err));
  });
  client.on('timeout', function() {
    console.log('Socket Timed out');
  });
});
server.listen(19882, function() {
  console.log('Server listening: ' + JSON.stringify(server.address()));
  server.on('close', function(){
    console.log('Server Terminated');
  });
  server.on('error', function(err){
    console.log('Server Error: ', JSON.stringify(err));
  });
});

var serverBus = net.createServer(function(client) {
  console.log('Client connection: ');
  console.log('   local = %s:%s', client.localAddress, client.localPort);
  console.log('   remote = %s:%s', client.remoteAddress, client.remotePort);
  client.setTimeout(1500);
  client.on('data', function(data) {
    if(data.toString().substr(0,4) == "/9j/"){
      image = '';
    }
    image += data.toString();
    var sendLength = '';
    if(sendDataBus.length > 0){
      if(sendDataBus.length < 10){
        sendLength = '0' + sendDataBus.length
      }
      sendDataBus = sendLength + sendDataBus;
      writeData(client, sendDataBus);
      console.log("send data to pi " + sendDataBus + " " + sendDataBus.length)
      sendDataBus = "";
    }
  });
  client.on('end', function() {
    console.log('Client disconnected');
    serverBus.getConnections(function(err, count){
      console.log('Remaining Connections: ' + count);
    });
  });
  client.on('error', function(err) {
    console.log('Socket Error: ', JSON.stringify(err));
  });
  client.on('timeout', function() {
    console.log('Socket Timed out');
  });
});
serverBus.listen(19883, function() {
  console.log('Server listening: ' + JSON.stringify(serverBus.address()));
  serverBus.on('close', function(){
    console.log('Server Terminated');
  });
  serverBus.on('error', function(err){
    console.log('Server Error: ', JSON.stringify(err));
  });
});

function writeData(socket, data){
  var success = !socket.write(data);
  if (!success){
    (function(socket, data){
      socket.once('drain', function(){
        writeData(socket, data);
      });
    })(socket, data);
  }
}

app.io.on('connection', function(socket){
  socket.on('disconnect', function(){
    console.log("disconnect : " + socket.id);
  });
  socket.on('image', function(data){
    if(image.length > 4000){
      socket.emit('image', {image: true, buffer: image});
    }
  });
  socket.on('image2', function(data){
    if(imageBus.length > 4000){
      socket.emit('image2', {image: true, buffer: imageBus});
    }
  });
});

module.exports = app;

