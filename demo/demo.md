# Docker Image Transfer Demo

### Load the Image on the Other Machine

On the target machine, navigate to the folder where you copied the file and run:

```bash
docker load < translate_api_0.1.0.tar.gz
```

### Verify

After loading, verify the image is available on the new machine:

```bash
docker image ls
```

You should see `localhost/translate` with the tag `0.1.0` in the list.

---

### Run the Container

Now you can run the container on the new machine:

```bash
docker run --rm -d -p 8000:8000 --name translation-api translate:0.1.0
```
