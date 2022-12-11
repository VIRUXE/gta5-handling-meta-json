# Convert an `handling.meta` file to *JSON* format
Why? Because I wanted to use the data in a web app. I'm sure there are other reasons. Maybe use it for a FiveM resource? I don't know.

## How it's done
I extracted all `vehicles.meta` and `handling.meta` files from the game
Built a dictionary with all the models that use a specific handling id
Sanitize each vehicle entry in the `handling.meta` files to make it a proper *JSON* format
Merge it all together to make a `handling.meta.json` that you can pretty much use anywhere where you would need the game's handling metadata
### Structure
```
{
    "HANDLINGID" = [
        "models" = {"model", ...},
        "data"   = {...}
    ],
    "HANDLINGID" = [
        "models" = {"model", ...},
        "data"   = {...}
    ]
}
```

## File `handling_models.json`
This file is a compiled list of vehicle models that use a specified handling id. Maybe that's all you would need...

### Structure
`"HANDLINGID" = [model, ...]`
