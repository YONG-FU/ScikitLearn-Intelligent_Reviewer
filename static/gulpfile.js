/// <binding Clean='clean' />
"use strict";

var gulp = require("gulp"),
    rimraf = require("rimraf"),
    concat = require("gulp-concat"),
    cssmin = require("gulp-cssmin"),
    uglify = require("gulp-uglify"),
    livereload = require('gulp-livereload');

var paths = {
    webroot: "./"
};

paths.js = paths.webroot + "js/*.js";
paths.minJs = paths.webroot + "**/*.min.js";
paths.minhereJs = paths.webroot + "**/*.js";
paths.css = paths.webroot + "css/*.css";
paths.minCss = paths.webroot + "**/*.min.css";
paths.minhereCss = paths.webroot + "**/*.css";
paths.concatJsDest = paths.webroot + "js/app.min.js";
paths.concatCssDest = paths.webroot + "css/site.min.css";

gulp.task("clean:js", function (cb) {
    rimraf(paths.concatJsDest, cb);
});

gulp.task("clean:css", function (cb) {
    rimraf(paths.concatCssDest, cb);
});

gulp.task("clean", ["clean:js", "clean:css"]);

gulp.task("min:js", function () {
    return gulp.src([paths.js, "!" + paths.minJs], { base: "." })
        .pipe(concat(paths.concatJsDest))
        .pipe(uglify())
        .pipe(gulp.dest("."));
});

gulp.task("min:css", function () {
    return gulp.src([paths.css, "!" + paths.minCss])
        .pipe(concat(paths.concatCssDest))
        .pipe(cssmin())
        .pipe(gulp.dest("."));
});

gulp.task("minhere:js", function () {
    return gulp.src([paths.minJs], { base: "." })
        // .pipe(concat(paths.concatJsDest))
        .pipe(uglify())
        .pipe(gulp.dest("."));
});

gulp.task("minhere:css", function () {
    return gulp.src([paths.minCss])
        // .pipe(concat(paths.concatCssDest))
        .pipe(cssmin())
        .pipe(gulp.dest("."));
});

gulp.task("min", ["min:js", "min:css"]);
gulp.task("minhere", ["minhere:js", "minhere:css"]);

gulp.task('js', function () {
    gulp.src(paths.js)
      .pipe(livereload());
});

gulp.task('css', function () {
    gulp.src(paths.css)
      .pipe(livereload());
});

gulp.task('html', function () {
    gulp.src('*.html')
      .pipe(livereload());
});


gulp.task('watch', function () {
    livereload.listen();
    gulp.watch(paths.js, ['js']);
    gulp.watch(paths.css, ['css']);
    gulp.watch('*.html', ['html']);
});
