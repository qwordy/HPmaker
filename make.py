#!/usr/bin/python3
import jinja2, yaml, shutil, os, markdown

def main():
  shutil.rmtree('output', True)
  os.mkdir('output')
  shutil.copy('template/bootstrap.min.css', 'output')
  shutil.copy('template/style.css', 'output')

  with open('content/config.yaml', 'r') as f:
    config = yaml.load(f)
  env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))
  md = markdown.Markdown()

  # Generate index.html
  with open('content/index.md', 'r') as f:
    html = md.convert(f.read())
  config['nav'] = 'index'
  config['text'] = html
  template = env.get_template('page.html')
  output = template.render(config)
  with open('output/index.html', 'w') as f:
    f.write(output)

  # Generate articles
  config['nav'] = None
  for root, _, files in os.walk('content'):
    for file in files:
      if file.endswith('.md') and file != 'index.md':
        print(file)
        with open(os.path.join(root, file), 'r') as f:
          state = 0
          meta = text = ''
          for line in f:
            if line == '---\n':
              state += 1
            elif state == 1:
              meta += line
            elif state == 2:
              text += line
          print(meta)
          print(text)


        ''' with open(os.path.join(root, file), 'r') as f:
          meta = yaml.load_all(f)
          print(meta)
          for m in meta:
            print(1)
        with open(os.path.join(root, file), 'r') as f:    
          html = md.convert(f.read())
          print(html) '''
        

main()