# Generated on 2013-11-27 using generator-angular 0.6.0-rc.2
"use strict"

require "shelljs/global"

# # Globbing
# for performance reasons we're only matching one level down:
# 'test/spec/{,*/}*.js'
# use this if you want to recursively match all subfolders:
# 'test/spec/**/*.js'
module.exports = (grunt) ->
  
  # Load grunt tasks automatically
  require("load-grunt-tasks") grunt
  
  # Time how long tasks take. Can help when optimizing build times
  require("time-grunt") grunt
  
  # Define the configuration for all the tasks
  grunt.initConfig
    
    # Project settings
    yeoman:
      
      # configurable paths
      app: require("./bower.json").appPath or "app"
      tmp: ".tmp"
      dist: "dist"
      backend:
        src: "backend/src"
        bin: "backend/bin"
        baseUrl: ""

    
    # Watches files for changes and runs tasks based on the changed files
    watch:
      coffee:
        files: ["<%= yeoman.app %>/scripts/{,**/}*.{coffee,litcoffee,coffee.md}"]
        tasks: ["newer:coffee:dist"]

      appCoffee:
        files: ["<%= yeoman.app %>/scripts/app.coffee"]
        tasks: ["replaceBackend"]

      coffeeTest:
        files: ["test/spec/{,**/}*.{coffee,litcoffee,coffee.md}"]
        tasks: [
          "newer:coffee:test"
          "karma"
        ]

      jade:
        files: ["<%= yeoman.app %>/{,**/}*.jade"]
        tasks: ["newer:jade:dist"]

      less:
        files: ["<%= yeoman.app %>/styles/{,**/}*.less"]
        tasks: ["newer:less:dist"]

      stylus:
        files: ["<%= yeoman.app %>/styles/{,**/}*.styl"]
        tasks: ["newer:stylus:dist"]

      cson:
        files: ["<%= yeoman.app %>/api/{,**/}*.cson"]
        tasks: ["newer:cson:dist"]

      styles:
        files: ["<%= yeoman.app %>/styles/{,**/}*.css"]
        tasks: [
          "newer:copy:styles"
          "autoprefixer"
        ]

      index:
        files: ["<%= yeoman.app %>/index.jade"]
        tasks: ["newer:jade:index"]

      python:
        files: ["<%= yeoman.backend.src %>/{,**/}*.py"]
        tasks: ["supervisord"]

      gruntfile:
        files: ["Gruntfile.coffee"]

      livereload:
        options:
          livereload: "<%= connect.options.livereload %>"

        files: [
          "<%= yeoman.app %>/{,**/}*.html"
          "<%= yeoman.tmp %>/styles/{,**/}*.css"
          "<%= yeoman.app %>/images/{,**/}*.{png,jpg,jpeg,gif,webp,svg}"
        ]

    
    # The actual grunt server settings
    connect:
      options:
        port: 9000
        
        # Change this to '0.0.0.0' to access the server from outside.
        hostname: "localhost"
        livereload: 35729

      livereload:
        options:
          #open: true
          open: false  # for grunt-open
          base: [
            "<%= yeoman.tmp %>"
            "<%= yeoman.app %>"
          ]

      test:
        options:
          port: 9001
          base: [
            "<%= yeoman.tmp %>"
            "test"
            "<%= yeoman.app %>"
          ]

      dist:
        options:
          base: "<%= yeoman.dist %>"

    open:
      all:
        url: "http://localhost:<%= connect.options.port %>"
        app: "/usr/share/iron/iron"

    # Make sure code styles are up to par and there are no obvious mistakes
    jshint:
      options:
        jshintrc: ".jshintrc"
        reporter: require("jshint-stylish")

      all: ["Gruntfile.js"]  #TODO Gruntfile.coffee

    
    # Empties folders to start fresh
    clean:
      dist:
        files: [
          dot: true
          src: [
            "<%= yeoman.tmp %>"
            "<%= yeoman.dist %>/*"
            "!<%= yeoman.dist %>/.git*"
          ]
        ]

      server: "<%= yeoman.tmp %>"

    
    # Add vendor prefixed styles
    autoprefixer:
      options:
        browsers: ["last 1 version"]

      dist:
        files: [
          expand: true
          cwd: "<%= yeoman.tmp %>/styles/"
          src: "{,**/}*.css"
          dest: "<%= yeoman.tmp %>/styles/"
        ]

    
    # Compiles CoffeeScript to JavaScript
    coffee:
      options:
        sourceMap: true
        sourceRoot: ""

      dist:
        files: [
          expand: true
          cwd: "<%= yeoman.app %>/scripts"
          src: "{,**/}*.coffee"
          dest: "<%= yeoman.tmp %>/scripts"
          ext: ".js"
        ]

      test:
        files: [
          expand: true
          cwd: "test/spec"
          src: "{,**/}*.coffee"
          dest: "<%= yeoman.tmp %>/spec"
          ext: ".js"
        ]

    jade:
      dist:
        files: [
          expand: true
          cwd: "<%= yeoman.app %>/views"
          src: "{,**/}*.jade"
          dest: "<%= yeoman.tmp %>/views"
          ext: ".html"
        ]

      index:
        options:
          pretty: true  # for collapse comment for uglify

        files: [
          expand: true
          cwd: "<%= yeoman.app %>"
          src: "index.jade"
          dest: "<%= yeoman.tmp %>"
          ext: ".html"
        ]

    less:
      dist:
        options:
          paths: [
            "<%= yeoman.app %>/bower_components/bootstrap/less"
            "<%= yeoman.app %>/styles"
          ]
          compress: false  #TODO

        files: [
          expand: true
          cwd: "<%= yeoman.app %>/styles"
          src: "{,**/}*.less"
          #src: "bootstrap.less"
          dest: "<%= yeoman.tmp %>/styles"
          ext: ".css"
        ]
    
    stylus:
      dist:
        files: [
          expand: true
          cwd: "<%= yeoman.app %>/styles"
          src: "{,**/}*.styl"
          dest: "<%= yeoman.tmp %>/styles"
          ext: ".css"
        ]
    
    cson:
      dist:
        files: [
          expand: true
          cwd: "<%= yeoman.app %>/api"
          src: "{,**/}*.cson"
          dest: "<%= yeoman.tmp %>/api"
          rename: (dest, src) ->
            dest + '/' + src.replace(/\.cson/, '')
        ]
    
    'string-replace':
      backend:
        files:
          "<%= yeoman.tmp %>/scripts/app.js": "<%= yeoman.tmp %>/scripts/app.js"

        options:
          replacements: [
            pattern: /%BASE_URL%/g
            replacement: "<%= yeoman.backend.baseUrl %>"
          ]


    # Renames files for browser caching purposes
    rev:
      dist:
        files:
          src: [
            "<%= yeoman.dist %>/scripts/{,**/}*.js"
            "<%= yeoman.dist %>/styles/{,**/}*.css"
            "<%= yeoman.dist %>/images/{,**/}*.{png,jpg,jpeg,gif,webp,svg}"
            "<%= yeoman.dist %>/styles/fonts/*"
          ]

    
    # Reads HTML for usemin blocks to enable smart builds that automatically
    # concat, minify and revision files. Creates configurations in memory so
    # additional tasks can operate on them
    useminPrepare:
      html: "<%= yeoman.app %>/index.html"
      options:
        dest: "<%= yeoman.dist %>"

    
    # Performs rewrites based on rev and the useminPrepare configuration
    usemin:
      html: ["<%= yeoman.dist %>/{,**/}*.html"]
      css: ["<%= yeoman.dist %>/styles/{,**/}*.css"]
      options:
        assetsDirs: ["<%= yeoman.dist %>"]

    
    # The following *-min tasks produce minified files in the dist folder
    imagemin:
      dist:
        files: [
          expand: true
          cwd: "<%= yeoman.app %>/images"
          src: "{,**/}*.{png,jpg,jpeg,gif}"
          dest: "<%= yeoman.dist %>/images"
        ]

    svgmin:
      dist:
        files: [
          expand: true
          cwd: "<%= yeoman.app %>/images"
          src: "{,**/}*.svg"
          dest: "<%= yeoman.dist %>/images"
        ]

    htmlmin:
      dist:
        options: {}
        
        # Optional configurations that you can uncomment to use
        # removeCommentsFromCDATA: true,
        # collapseBooleanAttributes: true,
        # removeAttributeQuotes: true,
        # removeRedundantAttributes: true,
        # useShortDoctype: true,
        # removeEmptyAttributes: true,
        # removeOptionalTags: true*/
        files: [
          expand: true
          cwd: "<%= yeoman.app %>"
          src: [
            "*.html"
            "views/*.html"
          ]
          dest: "<%= yeoman.dist %>"
        ]

    
    # Allow the use of non-minsafe AngularJS files. Automatically makes it
    # minsafe compatible so Uglify does not destroy the ng references
    ngmin:
      dist:
        files: [
          expand: true
          cwd: "<%= yeoman.tmp %>/concat/scripts"
          src: "*.js"
          dest: "<%= yeoman.tmp %>/concat/scripts"
        ]

    
    # Replace Google CDN references
    cdnify:
      dist:
        html: ["<%= yeoman.dist %>/*.html"]

    
    # Copies remaining files to places other tasks can use
    copy:
      dist:
        files: [
          {
            expand: true
            dot: true
            cwd: "<%= yeoman.app %>"
            dest: "<%= yeoman.dist %>"
            src: [
              "*.{ico,png,txt}"
              ".htaccess"
              "bower_components/**/*"
              "images/{,**/}*.{webp}"
              "fonts/*"
            ]
          }
          {
            expand: true
            cwd: "<%= yeoman.tmp %>/images"
            dest: "<%= yeoman.dist %>/images"
            src: ["generated/*"]
          }
        ]

      styles:
        expand: true
        cwd: "<%= yeoman.app %>/styles"
        dest: "<%= yeoman.tmp %>/styles/"
        src: "{,**/}*.css"

      glyphicons:
        expand: true
        cwd: "<%= yeoman.app %>/bower_components/bootstrap/fonts"
        dest: "<%= yeoman.tmp %>/fonts/"
        src: "{,**/}*"

    
    # Run some tasks in parallel to speed up the build process
    concurrent:
      server: [
        "coffee:dist"
        "jade:index"
        "jade:dist"
        "less:dist"
        "stylus:dist"
        "cson:dist"
        "copy:styles"
        "copy:glyphicons"
      ]
      test: [
        "coffee"
        "jade"
        "copy:styles"
        "copy:glyphicons"
      ]
      dist: [
        "coffee"
        "jade"
        "less"
        "stylus"
        #"cson"  #TODO
        "copy:styles"
        "copy:glyphicons"
        "imagemin"
        "svgmin"
        "htmlmin"
      ]

    
    # By default, your `index.html`'s <!-- Usemin block --> will take care of
    # minification. These next options are pre-configured if you do not wish
    # to use the Usemin blocks.
    # cssmin: {
    #   dist: {
    #     files: {
    #       '<%= yeoman.dist %>/styles/main.css': [
    #         '<%= yeoman.tmp %>/styles/{,*/}*.css',
    #         '<%= yeoman.app %>/styles/{,*/}*.css'
    #       ]
    #     }
    #   }
    # },
    # uglify: {
    #   dist: {
    #     files: {
    #       '<%= yeoman.dist %>/scripts/scripts.js': [
    #         '<%= yeoman.dist %>/scripts/scripts.js'
    #       ]
    #     }
    #   }
    # },
    # concat: {
    #   dist: {}
    # },
    
    # Test settings
    karma:
      unit:
        configFile: "karma.conf.js"
        singleRun: false
        autoWatch: true

  grunt.registerTask "serve", (target) ->
    if target is "dist"
      return grunt.task.run([
        "build"
        "connect:dist:keepalive"
      ])
    grunt.task.run [
      "clean:server"
      "concurrent:server"
      "replaceBackend"  #XXX backend
      "autoprefixer"
      "connect:livereload"
      "open"
      "watch"
    ]

  grunt.registerTask "server", ->
    grunt.log.warn "The `server` task has been deprecated. Use `grunt serve` to start a server."
    grunt.task.run ["serve"]

  grunt.registerTask "test", [
    "clean:server"
    "concurrent:test"
    "autoprefixer"
    "connect:test"
    "karma"
  ]
  grunt.registerTask "build", [
    "clean:dist"
    "useminPrepare"
    "concurrent:dist"
    "replaceBackend"  #XXX backend
    "autoprefixer"
    "concat"
    "ngmin"
    "copy:dist"
    "cdnify"
    "cssmin"
    "uglify"
    "rev"
    "usemin"
  ]
  grunt.registerTask "default", [
    "newer:jshint"
    "test"
    "build"
  ]

  # Pyramid supervisord
  grunt.registerTask "supervisord", ->
    exec grunt.config.get('yeoman.backend.bin') + "/supervisorctl reload", silent:true

  # Backend
  grunt.registerTask "replaceBackend", ->
    if grunt.option 'backend'
      baseUrl = '//' + grunt.option('backend')
    else
      baseUrl = ''
    grunt.config.set 'yeoman.backend.baseUrl', baseUrl
    grunt.task.run ["string-replace:backend"]

