var gulp = require('gulp');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');
var minifyCss = require('gulp-minify-css');

gulp.task('concat-client', function() {
  return gulp.src(['./clientlibs/web_client/js/app.js', './clientlibs/web_client/js/service.js', './clientlibs/web_client/js/controller.js', './clientlibs/web_client/js/directive.js'])
    .pipe(concat('culverbox.min.js'))
    .pipe(gulp.dest('./clientlibs/web_client/concat/'));
});


gulp.task('min-js-client', function() {
	return gulp.src('clientlibs/web_client/concat/culverbox.min.js')
    .pipe(uglify())
    .pipe(gulp.dest('clientlibs/web_client/min/'));
});

// gulp.task('min-css-client', function() {
//   return gulp.src('clientlibs/dep/culverStyles.css')
//     .pipe(gulp.dest('buyerlibs/min/'));
// });



gulp.task('default', ['concat-client', 'min-js-client']);