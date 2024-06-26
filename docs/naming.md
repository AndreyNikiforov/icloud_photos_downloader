# File Naming

Assets on iCloud have names. When downloading assets, `icloudpd` can adjust names.

## Folder Structure

```{versionchanged} 1.7.0
Support for `none` value added
```

`icloudpd` uses asset metadata (_created date_) to build folder hierarchy, and it can be adjusted with `--folder-stucture` parameter.

Specifying `--folder-structure none` will put all files into one folder.

## Duplicates

```{versionchanged} 1.20.0
`--file-match-policy` parameter added and `name-id7` policy implemented
```

In large iCloud collections it is possible to have name collisions. To avoid collisions if files need to be downloaded into the same folder, use `--file-match-policy` parameter:
- add unique invariant asset identification suffix to the name (e.g. **"IMG_1234_QAZXSW.JPG"**) with `--file-match-policy name-id7`
- de-duplicate by adding file size as a suffix (e.g. **"IMG_1234-67890.JPG"** for second asset); `--file-match-policy name-size-dedup-with-suffix` - it is default

## Live Photos

```{versionchanged} 1.18.0
`--live-photo-mov-filename-policy` parameter added and `original` policy implemented
```

Live Photo assets have two components: still image and short video. `icloudpd` can download both and allows customizing file name of the video portion with `--live-photo-mov-filename-policy` parameter:

- Use video file name the same as still image with `original` policy; use `--file-match-policy name-id7` to avoid clashes of video file with other videos.
- Use suffix from the still image with `suffix` policy: **"IMG_1234_HEVC.MOV"** for **"IMG_1234.HEIC"** still. This is default and works for HIEC still images only

## Unicode

```{versionchanged} 1.18.0
`--keep-unicode-in-filenames` parameter flag added with default `false` 
```

Unicode characters are stripped from file names for better compatibility. `icloudpd` can leave them when `--keep-unicode-in-filenames` is specified.
