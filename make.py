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
  

main()