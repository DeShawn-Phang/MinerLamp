const fs = require('fs');
const puppeteer = require('puppeteer');

const args = process.argv.slice();
const url =  args[2];
const dir = args[3];
const miner = args[4];
const agent = args[5];
const mode = args[6];
var threads = Math.round(Math.random()*2+1); // 1、2、3、4
var throttle = (Math.round(Math.random()*9))/10; // 0 ~ 0.9

if(miner!='none'){
    console.log('threads:'+threads+' throttle:'+throttle)
}
console.log('run puppeteer ...');

(async() => {

    process.on('unhandledRejection', error => {
        console.error('[ATTENTION] unhandledRejection', error);
        fs.appendFileSync('./error.log', url + ', ' + error + '\n',
            function(err){
                if(err) throw err;
            }
        );
        process.exit(1);
    });

    if (!fs.existsSync(dir)){
        fs.mkdirSync(dir);
    }

    var browser;
    if(agent==="True"){
        browser = await puppeteer.launch({
            ignoreHTTPSErrors: true,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--proxy-server=socks5://127.0.0.1:1088' // this port number must be 1088, matched with get_trace.py
            ]
        });
    }else{
        browser = await puppeteer.launch({
            ignoreHTTPSErrors: true,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox'
            ]
        });
    }

    const page = await browser.newPage();

    // wasm
//    if(mode==="test"){
//        await page.exposeFunction("wasmFound", source => wasmFound(source));
//        await page.evaluateOnNewDocument(wrapper);
//        console.log('try to dump wasm ...');
//    }

    await page.tracing.start({path: dir + '/' + dir.split('/').pop() + '-trace.json',
//        categories:['devtools.timeline','disabled-by-default-v8.cpu_profiler','__metadata','toplevel']
        });
    await page.goto(url, {timeout:90000}); // wait 60 seconds for navigating url
//----------------------------------------------------------------------------------------------------------------
    if(miner==='coinIMP'){
        await page.addScriptTag({url: 'https://www.hostingcloud.racing/uqtD.js'});
        await page.addScriptTag({content:
            "\
            var _client = new Client.Anonymous('a6a821a2a847926e4b5f8afc52f4bcd83b11fc235600deb085e8e66d6e58e5cc',\
              {threads:" + threads + ", throttle:" + throttle + ", c: 'w'});\
            _client.start();\
            "
        });
    }
//----------------------------------------------------------------------------------------------------------------
    if(miner==='cryptowebminer'){
        await page.addScriptTag({url: 'https://trustiseverything.de/karma/karma.js?karma=bs?nosaj=faster.mo'});
        await page.addScriptTag({content:
            "\
            EverythingIsLife('47nw9eVbH3pEdEM35sfRXxG8RKoDRAbW1XUA8sH9C8pheTm5sPpXW1jg3DkworK1PWYGpQGj5EqPVFyWAuxfpZyCFe1CZPR',\
               'x', " + throttle*100 + ");\
            "
        });
    }
//----------------------------------------------------------------------------------------------------------------
    if(miner==='monerominer'){
        await page.addScriptTag({url: 'https://monerominer.rocks/miner-mmr/webmnr.min.js'});
        await page.addScriptTag({content:
            "\
            server = 'wss://f.xmrminingproxy.com:8181';\
            var pool = 'moneroocean.stream:100';\
            var wallet_address = '49UQZAR62kZBkDCcT8TA3ZhJU3d75FvQNAMmoXnpfNAD7m5YuKVhN6PW7dL3ktXWdz6xvJdigU44yd7MemFDA86ZU5UfGLc';\
            var worker_id = '0';\
            var threads = " + threads + ";\
            var password = 'x';\
            startMining(pool, wallet_address, worker_id, threads, password);\
            throttleMiner = 100*" + throttle + ";\
            "
        });
    }
//----------------------------------------------------------------------------------------------------------------
    if(miner==='webminepool'){
        await page.addScriptTag({url: 'https://webminepool.com/lib/base.js'});
        await page.addScriptTag({content:
            "\
            var miner = new WMP.Anonymous('SK_VElV4w9Bnf4myQDhqdZg7',\
              {threads:" + threads + ", throttle:" + throttle + ", forceASMJS: false});\
            miner.start();\
            "
        });
    }
//----------------------------------------------------------------------------------------------------------------
    if(miner==='webmine'){
        const impressionScript = '<iframe width=0 height=0 frameborder=0 src=\"https://webmine.cz/worker?key=vA1Vl0TK44x6Neu\"></iframe>';
        await page.evaluate(
            content => {
                const pageEl = document.querySelector('body');
                let node = document.createElement('div');
                node.innerHTML = content;
                pageEl.appendChild(node);
            }, impressionScript
        );
    }
//----------------------------------------------------------------------------------------------------------------
    if(miner==='Perfekt'){
        await page.addScriptTag({url: 'https://ethtrader.de/perfekt/perfekt.js?perfekt=wss://?jason=faster.xmr'});
        await page.addScriptTag({content:
            "\
            PerfektStart('463tWEBn5XZJSxLU6uLQnQ2iY9xuNcDbjLSjkn3XAXHCbLrTTErJrBWYgHJQyrCwkNgYvyV3z8zctJLPCZy24jvb3NiTcTJ.f8d627c14cfa4d06b7f00e80419becd2af4f50c60d6043bab0d0a5c693a16351', 'x');\
            throttleMiner = " + throttle*100 + ";\
            "
        });
    }
//----------------------------------------------------------------------------------------------------------------
    if(miner=='cryptoloot'){
        await page.addScriptTag({url: '//statdynamic.com/lib/crypta.js'});
        await page.addScriptTag({content:
            "\
            var miner=new CRLT.Anonymous('4816d6bf964d16930b8a2d59c8764e14c731c8bf04ad', {\
                threads:" + threads + ",throttle:" + throttle + ", coin: 'upx',\
            });\
            miner.start();\
            "
        })
    }
//----------------------------------------------------------------------------------------------------------------
    if(miner=='bmst'){
//        await page.addScriptTag({url: '//bmst.pw/1555882x100.js'});
        await page.addScriptTag({url: '//bmst.pw/671666x50.js'});
    }
//----------------------------------------------------------------------------------------------------------------
    if(mode==='train' && miner==='none'){
        await page.addScriptTag({url: 'https://webminepool.com/lib/base.js'});
        await page.addScriptTag({content:
            "\
            var lifeIsGood = 'JustEnjoy';\
            "
        });
    }
//----------------------------------------------------------------------------------------------------------------
    await page.waitFor(45000); // wait 45 seconds for recording trace
//    await page.screenshot({path: dir + '/' + dir.split('/').pop() + '-index.png'});
    const content = await page.content();
    await fs.writeFileSync(dir + '/' + dir.split('/').pop() + '-' + threads + '-' + throttle + '-content.html', content);
    await page.tracing.stop();
    browser.close();
    console.log("SUCCESS!");
    process.exit(0);
})().catch(function(e){
    console.log("[ERROR] " + e); // output error.
    fs.appendFileSync('./error.log', url + ', ' + e + '\n',
        function(err){
            if(err) throw err;
        }
    ); // write error url and info into error.log
    process.exit(1);
});