# Simple REST API

A simple REST API for uploading and serving images.

## Getting Started

### Prerequisites

Before starting, install [Compose](https://docs.docker.com/compose/install/).


### Installation

Clone the project repository.

```
$ git clone 
```

Go inside the top level directory of the project.

Create an `.env` file. There is an `.env.example` file available in the project directory.

Run the migrate command with docker compose.
```
$ sudo docker compose run web python manage.py migrate 
```

Run the docker compose up command.
```
$ docker compose up
```

## Usage

A few examples of useful commands and/or tasks.

### API endpoints

* POST `api/images/` - allows to upload an image. The 
* GET `api/images/` - returns a list of image objects. Allows filter by `title` to find objects with a title containing the provided string.
* GET `api/images/:id` - returns single image object based on id.
* GET `api/schema/swagger-ui/` - API documentation endpoint

### POST `api/images/` 

Endpoint allows to upload an image and creates a new Image object.
The following data can be specified:

*  `title` - title string 
*  `width` - width in pixels (should be lower than original image width),
*  `height` - height in pixels (should be lower than original image height),
*  `image` - uploaded image,
*  `keep_ratio` - true/false value. If true, the image will keep the original aspect ratio.

Either `width` or `height` (or both) must be provided. If only one dimension value is given, the image will be scaled according to it (proportionally).

If the `width` and `height` will be greater than original image dimensions, the image will not be scaled. Instead, it will be saved in its original size.

## Testing

The tests can be run with following command:
```
$ sudo docker compose run web pytest -v
```
