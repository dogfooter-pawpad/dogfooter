const express = require('express');
const WebSocket = require('ws');
const path = require('path');
const http = require('http');

///* Store the message from client */
//var messageServer = [];
//var factorialResult = 0;
//
///* Server port */
//const PORT = process.env.PORT || 18091;
///* Tell express to deliver files found in this folder*/
//const PUBLIC  = path.join(__dirname, 'public');
//
//const app = express()
//    .use(express.static(PUBLIC));
//
///* Initialize an http server */
//const server = http.createServer(app);
//
///* Initialize the WebSocket server instance */
//const wss = new WebSocket.Server({ server });
//
///* Server port */
//server.listen(PORT, function listening() {
////    console.log('Listening on %d', server.address().port);
//  });
//
///* On any connection */
//wss.on('connection', (connection, req) => {
//    /* Connection is OK then add an event */
////    console.log(req.client);
//    connection.on('message', (message) => {
//        /* Log the received message */
////        console.log(`Message received from client: ${message}`);
////        connection.send('----------------------------------------------------------')
//    });
//    connection.on('close', (connection) => {
//        console.log('연결끊김:');
//        process.exit()
//    });
//    console.log('도그푸터 매크로 로그인에 성공했습니다.');
//});

//const fs = require('fs');
//const pip_user_file_path = './pip-user.json';
//const pip_file_path = './pip.json';
//const git_file_path = './.git';
//const vbs_file_path = './도그푸터 바로 실행.vbs';
//let pip_user = null;
//let branch = 'master'
//if ( process.argv.length > 2 ) {
//    branch = process.argv[2]
//} else {
//    console.log('게임을 선택해야 합니다.');
//    console.log('실행방법> node dogfooter.js <게임코드명>');
//    process.exit()
//}

const execSync = require('child_process').execSync;

function check_l2m() {
    let child = spawn("cmd.exe", ['/c', 'cd D:\\pawpad\\macro && python repeat.py'], {
            detached: true,
        }
    )
    child.on('exit', function(code) {
        console.log(code);
        check_l2m()
    })
}
//if (fs.existsSync(pip_user_file_path)) {
//    try {
//        pip_user = JSON.parse(fs.readFileSync(pip_user_file_path, 'utf8'));
//    } catch (e) {
//        pip_user = null
//    }
//}
//
//if ( pip_user === null) {
//    pip_user = {}
//    // 처음 실행
//    console.log('도그푸터 초기화 중입니다...')
//    execSync('"python" -m pip install --upgrade pip', function(error, stdout, stderr) {
//        console.log(stdout);
//    });
//} else {
//    console.log('업데이트 확인 중입니다...')
//}
//
//try {
//    stdout = execSync('"git" rev-parse --abbrev-ref HEAD');
////    console.log('DEBUG2:', String.fromCharCode.apply(String, stdout));
//
//    if (!stdout.includes(branch)) {
//         fs.renameSync('./lyb.cfg', './lyb.cfg.' + ('' + stdout).replace(/\n/, '') + '.' +  (new Date()).toISOString().replace(/T/, ' ').replace(/\..+/, '').replace(' ', '').replace(/-/gi, '').replace(/:/gi, ''), function(err) {
//            if ( err ) console.log('ERROR: ' + err);
//        });
//    }
//} catch (e) {
//}
//
//try {
//    stdout = execSync('"git" checkout ' + branch);
//    const vbs_content = `
//Set WshShell = CreateObject("WScript.Shell" )
//WshShell.Run "node dogfooter.js ${branch}", 0
//Set WshShell = Nothing
//    `;
//    fs.writeFile(vbs_file_path, vbs_content, 'utf8', function(e) {
//
//    });
//} catch (e) {
//    console.log('게임코드명이 잘못됐습니다.(' + branch + ')');
//    process.exit();
//}
//
//execSync('"git" pull');
//
//let pipJson = null;
//if (fs.existsSync(pip_file_path)) {
//    pipJson = JSON.parse(fs.readFileSync(pip_file_path, 'utf8'));
//}
//
//if ( pipJson ) {
//    let pip = pipJson.pip;
//    for ( let i = 0; i < pip.length; i++ ) {
//        if ( !pip_user.hasOwnProperty(pip[i]) ) {
//            console.log('파이썬 모듈 업데이트 중입니다.')
//            pip_user[pip[i]] = true;
//            pip_command = '"pip" install ' + pip[i];
//            execSync(pip_command);
//        }
//    }
//}
//
//fs.writeFile(pip_user_file_path, JSON.stringify(pip_user), 'utf8', function(e) {});

/* Generate a python process using nodejs child_process module */
//const spawn = require('child_process').spawn;
//child = spawn('python', ['main.py'])

const exec = require('child_process').exec;
const spawn = require('child_process').spawn;
console.log('도그푸터 매크로 실행 중입니다. 잠시만 기다려주세요.')
const cmd1 = 'Start-Process cmd -Verb RunAs -ArgumentList'
const cmd2 = "'/c cd D:\\pawpad\\macro && python repeat.py'"
const cmd3 = 'powershell -Command "' + cmd1 + ' ' + cmd2 + '"'

console.log(cmd3)
check_l2m()

//exec(cmd3, function(error, stdout, stderr) {
//
//    console.log('python error:', error)
//    console.log('python stdout:', stdout)
//    console.log('python stderr:', stderr)
//exec('"python" main.py', function(error, stdout, stderr) {
//    console.log('python error:', error)
//    console.log('python stdout:', stdout)
//    console.log('python stderr:', stderr)

//    console.log('python error:', error)
//    process.exit()
//});