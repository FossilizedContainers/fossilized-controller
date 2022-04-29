source("adapter.R")

fakeModel = function(adapter) {
  library(ggplot2)

  data(iris)

  simple.plot <-ggplot(data=iris,
                       aes(x=Sepal.Width,
                           y=Sepal.Length,color=Species)) + 
    geom_point() + 
    theme_minimal()

  complex.plot <- ggplot(data=iris,
                         aes(x=Sepal.Width,
                             y=Sepal.Length,color=Species)) + 
    geom_point() + 
    geom_smooth(se=FALSE) + 
    theme_minimal()

  if (adapter$parameters$figtype == "simple") {
    ggsave(simple.plot, file="output.png" , width=4, height=4)
  } else {
    ggsave(complex.plot, file="output.png", width=4, height=4)
  }

  adapter$setOutputFiles("output.png")
}

global.adapter$register("fakeModel(global.adapter)")
global.adapter$startServer()
