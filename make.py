#!/usr/bin/python3
import shutil
import os
import jinja2
import yaml
import markdown

OUTPUT = 'output'
CONTENT = 'content'
TEMPLATE = 'template'


def loadConfig(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)


def writeFile(filename, str):
    """
    Write str to filename
    """
    with open(filename, 'w', encoding='utf8') as f:
        f.write(str)


def main():
    shutil.rmtree(OUTPUT, True)
    os.mkdir(OUTPUT)
    os.system('cp ' + TEMPLATE + '/*.css ' + OUTPUT)

    config = loadConfig(CONTENT + '/config.yaml')
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE))
    md = markdown.Markdown()

    # Generate CNAME
    writeFile(OUTPUT + '/CNAME', config['cname'])

    # Generate index.html
    with open(CONTENT + '/index.md', 'r', encoding='utf8') as f:
        html = md.convert(f.read())
    config['text'] = html
    template = env.get_template('page.html')
    output = template.render(config)
    writeFile(OUTPUT + '/index.html', output)

    # Generate articles
    template = env.get_template('article.html')
    posts = []
    generateArticles(CONTENT, posts, md, config, template)

    # Generate articles.html
    # Sort by date, post[2] is date
    posts.sort(key=lambda post: post[2], reverse=True)
    config['posts'] = posts
    template = env.get_template('articles.html')
    output = template.render(config)
    writeFile(OUTPUT + '/articles.html', output)


def generateArticles(root, posts, md, config, template):
    """
    Geretate articles in directory and sub-directories
    """
    # Remove CONTENT/
    subroot = root[len(CONTENT) + 1 :]
    if subroot != '':
        os.mkdir(OUTPUT + '/' + subroot)
    for f in os.listdir(root):
        fullname = os.path.join(root, f)
        # Directory
        if os.path.isdir(fullname):
            generateArticles(fullname, posts, md, config, template)
        # Regular file
        elif os.path.isfile(fullname):
            name, suffix = os.path.splitext(f)
            # Generate article
            if suffix == '.md' and name != 'index':
                post, text = parseMd(fullname, md)
                # If hide, then skip
                if 'hide' in post:
                    continue
                post['path'] = fullname[len(CONTENT) + 1 : -3] + '.html'
                post['text'] = text
                config['post'] = post
                output = template.render(config)
                writeFile(OUTPUT + '/' + post['path'], output)
                posts.append((post['title'], post['path'], post['date']))
            # Copy other file
            if suffix != '.md' and fullname != CONTENT + '/config.yaml':
                dstPath = OUTPUT + '/' + fullname[len(CONTENT) + 1 :]
                # print(fullname)
                # print(dstPath)
                shutil.copy(fullname, dstPath)


def parseMd(filename, md):
    """
    return meta, text
    """
    state = 0
    meta = text = ''
    for line in open(filename, encoding='utf8'):
        if line == '---\n':
            state += 1
        elif state == 1:
            meta += line
        elif state == 2:
            text += line
    meta = yaml.load(meta)
    text = md.convert(text)
    return meta, text


if __name__ == '__main__':
    main()
