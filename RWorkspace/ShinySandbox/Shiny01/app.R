##Load USGS Water Use data and enable visualization by state
# 1. Create table from URL (for a user specified year...) > useTbl
# 2. Load fips->stateName crosswalk table (fipsTbl), join with use data
# 3. Join data with State Map
# 4. Select attribute and show variable

#Load libraries
library(shiny)
library(dplyr)
library(magrittr)
library(ggplot2)
library(maps)
library(mapdata)

#Load data (remove last column named 'X', which is just an artifact)
theURL <- 'http://water.usgs.gov/watuse/data/2010/usco2010.txt'
dataTbl = read.table(theURL, sep='\t',header=TRUE) %>%
  select(-X) #Removes the "X" column

#Load the Fips remap table
theURL <- "https://raw.githubusercontent.com/johnpfay/WaterAccounting/ExploreData/RWorkspace/ShinySandbox/stfipstable.csv"
fipsTbl <- read.csv(theURL) %>%
  select(one_of(c("FIPS.Code","State.Name")))

#Join state names
dataTbl <- left_join(dataTbl,fipsTbl,by = c("STATEFIPS" = "FIPS.Code"))

#Drop non-data fields
dataTbl <- select(dataTbl,-(STATE:YEAR))

#Group records on states and compute sum of values
stateTbl = group_by(dataTbl,State.Name) %>%
  select(-contains("PCp")) %>% #Remove per-capita columns
  summarise_each(funs(mean(., na.rm = TRUE)))

#Remove dataTbl and fipsTbl
remove(dataTbl,fipsTbl)

#Generate a list of variables (skipping the first item: "State.Name")
useVars <- colnames(stateTbl)[-1]

# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("USGS Water use data"),
   
   # Sidebar with a slider input for number of bins 
   sidebarLayout(
      sidebarPanel(
         sliderInput("bins",
                     "Number of bins:",
                     min = 1,
                     max = 50,
                     value = 30),
         selectInput("useParam",
                     "Select parameter",
                     useVars)
      ),
      
      # Show a plot of the generated distribution
      mainPanel(
         plotOutput("distPlot")
      )
   )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
   
   output$distPlot <- renderPlot({
      # generate bins based on input$bins from ui.R
      x    <- faithful[, 2] 
      bins <- seq(min(x), max(x), length.out = input$bins + 1)
      
      # draw the histogram with the specified number of bins
      hist(x, breaks = bins, col = 'darkgray', border = 'white')
   })
}

# Run the application 
shinyApp(ui = ui, server = server)

