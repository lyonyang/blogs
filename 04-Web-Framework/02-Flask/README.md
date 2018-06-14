# Flask初识

[![Flask](https://img.shields.io/badge/flask%20version-0.12.2-blue.svg)](https://pypi.org/project/Flask/)
[![Python Versions](https://img.shields.io/badge/python-2.x%2C%203.x-blue.svg)](https://www.python.org/)

## 介绍

Flask是一个微型框架 , 它基于Python , 并且依赖着两个外部库 : Jinja2模板引擎和Werkzeug WSGI工具集

Flask的 "微" (Micro) 并不是意味着把整个Web应用放入到一个Python文件 , 尽管确实可以这么做 , 其主要时候指 , Flask旨在保持代码简介且易于扩展 , 所以Flaks不会为你做太多的选择 , 比如选择什么样的数据库 , 选择什么样的模板引擎 , 这些都取决你

默认情况下 , Flask并不包含数据库抽象层 , 表单验证或者任何其他现有库 (Django) 能处理的 , 相反 , Flask支持扩展 , 这些扩展能够添加功能到你的应用 , 就像是Flask本身实现的一样 . 众多的扩展提供了数据库集成 , 表单验证 , 上传处理 , 多种开放的认证技术等功能

Flask可能是 "微" 型的 , 但是它已经能够在各种各样的需求中生产使用

## 配置和约定

Flask有许多带有合理默认值的配置项 , 也遵循一些惯例 , 比如 : 按惯例 , 模板和静态文件存储在应用Python源代码树下的子目录中 , 模板文件夹名称与Django一样 "templates" , 静态文件夹名称 "static" 等等

总之 , Flask由于它的 "微" , 当然也可以说 "轻" , 使它得到的广泛的应用 , 便于扩展 , 而不像Django那样 , 强大却有时会显得笨重


https://python-team.gitbooks.io/flask-doc/content/di-yi-zhang-flask-jie-shao.html
