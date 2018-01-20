#!/usr/bin/python3
import shutil
import os
import jinja2
import yaml
import markdown

def loadConfig(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)


def writeFile(filename, str):
    with open(filename, 'w') as f:
        f.write(str)


def main():
    shutil.rmtree('output', True)
    os.mkdir('output')
    shutil.copy('template/bootstrap.min.css', 'output')
    shutil.copy('template/style.css', 'output')

    config = loadConfig('content/config.yaml')
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))
    md = markdown.Markdown()

    # Generate CNAME
    writeFile('output/CNAME', config['cname'])

    # Generate index.html
    with open('content/index.md', 'r') as f:
        html = md.convert(f.read())
    config['nav'] = 'index'
    config['text'] = html
    template = env.get_template('page.html')
    output = template.render(config)
    writeFile('output/index.html', output)

    # Generate articles
    config['nav'] = None
    template = env.get_template('article.html')
    posts = []
    for root, _, files in os.walk('content'):
        for file in files:
            name, suf = os.path.splitext(file)
            if suf == '.md' and name != 'index' and name != 'contents':
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
                meta = yaml.load(meta)
                text = md.convert(text)
                post = dict(meta)
                post['filename'] = name + '.html'
                post['text'] = text
                config['post'] = post
                output = template.render(config)
                writeFile('output/' + post['filename'], output)
                post = config['post']
                posts.append((post['title'], post['filename'], post['date']))
                # posts.append(post)

    # Generate contents
    config['nav'] = 'contents'
    config['posts'] = posts
    template = env.get_template('contents.html')
    output = template.render(config)
    writeFile('output/' + 'contents.html', output)


main()
