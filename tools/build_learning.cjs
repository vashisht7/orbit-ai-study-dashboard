const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'..');
require('node:child_process').execFileSync('python3',[path.join(root,'tools/build_transformer_notebooks.py')],{stdio:'inherit'});
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const sandbox={window:{}};
vm.runInNewContext(read('beginner/course.js'),sandbox);
const labs={};for(const c of sandbox.window.BEGINNER){if(c.lab&&fs.existsSync(path.join(root,'beginner/labs',c.lab)))labs[c.id]=read('beginner/labs/'+c.lab);}
let resume=read('ai-depth/resume-path.js');let raw=resume.split('const paths=')[1].split('\n  const esc=')[0].trim().replace(/;$/,'');
const paths=vm.runInNewContext('('+raw+')');
const train=read('learning/model-workshop/train.py');
fs.writeFileSync(path.join(root,'learning/resources.js'),'window.LEARNING_RESOURCES='+JSON.stringify({labs,paths,train,workshop:read('learning/model-workshop/README.md')})+';\n');
console.log('Built lesson code, resume paths, and workshop source.');
require('node:child_process').execFileSync('python3',['-c',`import pathlib,zipfile
root=pathlib.Path(${JSON.stringify(root)})
with zipfile.ZipFile(root/'learning/model-workshop.zip','w',zipfile.ZIP_DEFLATED) as z:
 for name in ['train.py','sample.txt','README.md','requirements.txt','requirements-notebook.txt','Write_Your_Transformer.ipynb','Transformer_Reference.ipynb']:
  z.write(root/'learning/model-workshop'/name,'model-workshop/'+name)
`]);
console.log('Packaged the model workshop ZIP.');
