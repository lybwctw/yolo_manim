import os

import numpy as np
import torch


DIR_TENSOR = 'assets/tensor'
DIR_NUMPY = 'assets/numpy'


SF_SLICES = {
    8: slice(None, 6400),
    16: slice(6400, 8000),
    32: slice(8000, None),
}


OUTPUT_TYPES = (
    'box_raw',
    'box_softmax',
    'box_dist',
    'box_decode',
    'cls_raw',
    'cls_sigmoid',
)


def sf2dir(sf: int) -> str:
    size = 640 // sf
    return f'{sf:03d}_{size:02d}x{size:02d}'


def tensor_to_numpy(
    source_path: str,
    target_path: str,
    sf: int,
) -> None:
    tensor = torch.load(
        source_path,
        weights_only=True,
        map_location='cpu',
    )

    selected = tensor[0, :, SF_SLICES[sf]]

    result = (
        selected
        .transpose(0, 1)
        .reshape(640//sf, 640//sf, -1)
        .numpy()
    )

    # ensure directory exists
    os.makedirs(
        os.path.dirname(target_path),
        exist_ok=True,
    )

    np.save(target_path, result)

    print(f'saved: {target_path}')


if __name__ == "__main__":
    for sf in (8, 16, 32):
        for output_type in OUTPUT_TYPES:
            source_path = os.path.join(
                DIR_TENSOR,
                f'{output_type}.pt',
            )

            target_path = os.path.join(
                DIR_NUMPY,
                sf2dir(sf),
                f'{output_type}.npy',
            )

            tensor_to_numpy(
                source_path=source_path,
                target_path=target_path,
                sf=sf,
            )