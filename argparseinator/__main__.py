# -*- coding: utf-8 -*-
"""
===================
ArgParseInator Init
===================

Initialize a new python project based on ArgParseInator.
"""
from __future__ import absolute_import, print_function
import os
from os.path import join, basename, dirname, abspath, relpath, splitext
from string import Formatter
import sys
from argparseinator import ArgParseInator, arg, __version__
from argparseinator import get_compiled
import argparse
if sys.version_info >= (3, 0):
    basestring = str
CUR_DIR = abspath(os.curdir)
SKEL_PATH = join(abspath(dirname(__file__)), 'skeleton')


class DevFormatter(Formatter):
    """Formatter"""

    def __init__(self, name, dest, description=None):
        self.name = name
        wholetitle = "{} :core:`{}.{}`".format(
            name.title(), basename(dirname(dest)), name)
        wholetitlemark = "=" * len(wholetitle)
        description = description or ''
        self.info = dict(
            prj_name=name,
            prj_title=name.title(),
            prj_titlemark="=" * len(name.title()),
            mod_path=name,
            title=name.title(),
            titlemark="=" * len(name.title()),
            wholetitle=wholetitle,
            wholetitlemark=wholetitlemark,
            description=description,
        )
        super(DevFormatter, self).__init__()

    def get_value(self, key, args, kwargs):
        if key.endswith('-') and key.startswith('-'):  # formato mio?
            return kwargs[key[1:-1]]
        return "{" + key + "}"


def copy_skeleton(
        name, src, dest, renames=None, description=None, ignore=False,
        exclude_dirs=None, exclude_files=None):
    """Copy skeleton"""
    fmt = DevFormatter(name, dest, description=description)
    if os.path.exists(dest):
        if ignore is False:
            print("project already exists.")
            return 1
    else:
        os.makedirs(dest)
    renames = renames or []
    exclude_dirs = exclude_dirs or []
    exclude_files = exclude_files or []
    for root, dirs, files in os.walk(src, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [
            f for f in files if f not in exclude_files
            and not f.endswith('pyo') and not f.endswith('pyc')]
        for dname in [join(dest, d) for d in dirs if d]:
            for rsrc, rdest in renames:
                dname = dname.replace(rsrc, rdest)
            try:
                os.makedirs(dname)
            except Exception:
                pass
        for fname in files:
            sfile = join(root, fname)
            dfile = join(dest, relpath(sfile, src))
            for rsrc, rdest in renames:
                dfile = dfile.replace(rsrc, rdest)
            if os.path.exists(dfile):
                continue
            name = basename(splitext(dfile)[0])
            wholetitle = "{} :core:`{}.{}`".format(
                name.title(), basename(dirname(dfile)), name)
            wholetitlemark = "=" * len(wholetitle)
            fmt.info.update(dict(
                title=name.title(),
                titlemark="=" * len(name.title()),
                wholetitle=wholetitle,
                wholetitlemark=wholetitlemark,
                parentname=basename(dirname(dfile)),
            ))
            script = open(sfile, 'r').read()
            try:
                code = fmt.format(script, **fmt.info)
                open(dfile, 'w').write(code)
            except ValueError:
                pass


@arg("subnames", help="Subproject/Submodule name", nargs="*")
@arg("name", help="Project name")
@arg("-d", "--dest", default=None,
     help="destination path (default to current folder)")
@arg("-k", "--skeleton", default=None,
     help="skeleton path (default to argparseinator/skeleton folder)")
@arg("-t", "--project-type", default="standalone",
     choices=['standalone', 'subprojects', 'submodules'],
     help="Creates a subprojects structure.")
@arg("-s", "--skip-core", action="store_true",
     help="skips core package/folder creation")
@arg("-D", "--description", help="Project description")
def init(name, subnames, dest, skeleton, description, project_type, skip_core):
    """Creates a standalone, subprojects or submodules script sctrucure"""
    dest = dest or CUR_DIR
    skeleton = join(skeleton or SKEL_PATH, project_type)
    project = join(dest, name)
    script = join(project, name + '.py')
    core = join(project, name)
    if project_type == 'standalone':
        renames = [
            (join(project, 'project.py'), script),
            (join(project, 'project'), core)]
        copy_skeleton(
            name, skeleton, project, renames=renames, description=description,
            ignore=False)
    else:
        renames = [
            (join(project, 'project.py'), script),
            (join(project, 'project'), core)]
        exclude_dirs = ['submodule'] + (['project'] if skip_core else [])
        copy_skeleton(
            name, skeleton, project, renames=renames, description=description,
            exclude_dirs=exclude_dirs, ignore=True)
        for subname in subnames:
            renames = [
                (join(project, 'submodule'), join(project, subname))
            ]
            copy_skeleton(
                subname, skeleton, project, renames=renames,
                description=description, ignore=True,
                exclude_dirs=['project'], exclude_files=['project.py'])
    return 0, "\n{}\n".format(project)

if __name__ == '__main__':
    ArgParseInator(
        prog="python -margparseinator", auto_exit=True,

        show_defaults=False).check_command()
