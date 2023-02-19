import aiohttp
import logging
from asyncio import TimeoutError
from aiohttp import ClientError

from typing import List        # for type hints (python < 3.9)


logger = logging.getLogger(__name__)


async def get_text(url: str) -> str or None:
    """
    This function used to get text from url asyncio
    Args:
        url (str): our url to get data.
    Returns:
        (str | None): matrix as str.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if 400 <= response.status < 500:
                    logger.error("Client error.")
                elif response.status > 500:
                    logger.error("Server error.")
                else:
                    return await response.text()
                return await response.text()
    except ClientError as ex:
        logger.error(f"There are problems with connection {ex}.")
    except TimeoutError as ex:
        logger.error(f"Timeout error {ex}.")


def prepare_matrix(text: str) -> List[List[int]]:
    """
    This function used to transform text to raw matrix.
    Args:
        text (str): our text contains data.
    Returns:
        (list[list[int]]): matrix as list of lists.
    """
    try:
        matrix = []
        for line in text.split('\n'):
            if line and line[0] != '+':
                matrix.append([int(num) for num in line[1:-1].split('|')])

        if matrix and not all([len(matrix) == len(line) for line in matrix]):
            raise ValueError('Matrix is not squared.')
    except ValueError as ex:
        logger.warning(ex)
        return []
    return matrix


def traverse_matrix(matrix: List[List[int]], output: List[int]) -> List[int]:
    """
    This function used to traverse our matrix.
    Args:
        matrix (list[list[int]]): our matrix contains data;
        output (list[int]): empty list.
    Returns:
        (list[int]): matrix as a ready list[int].
    """
    # print(matrix, type(matrix[0]))
    if not len(matrix):
        return output
    matrix = [list(i) for i in list(zip(*matrix[::-1]))]
    output.extend(matrix[0][::-1])
    traverse_matrix(matrix[1:], output)


async def get_matrix(url: str) -> List[int]:
    """
    This function used to do all operations with matrix.
    Args:
        url (str): our url to get data.
    Returns:
        (list[int]): matrix as a ready list[int].
    """
    output = []
    text = await get_text(url)
    traverse_matrix(prepare_matrix(text), output)
    return output


if __name__ == '__main__':
    url = 'https://raw.githubusercontent.com/avito-tech/' \
          'python-trainee-assignment/main/matrix.txt'
