"""
Module about Pauli (and I) matrices.
"""

import numpy as np
from numpy import zeros_like

s0 = np.array([[1, 0], [0, 1]])
s1 = np.array([[0, 1], [1, 0]])
s2 = np.array([[0, -1j], [1j, 0]])
s3 = np.array([[1, 0], [0, -1]])

s0T = s0.T
s1T = s1.T
s2T = s2.T
s3T = s3.T

pauli_dict = {0: s0, 1: s1, 2: s2, 3: s3}


def pauli_mat(nbasis, i):
    """
    nbasis: size of the matrix. should be multiple of 2.
    i: index of pauli dictionary.
    """
    N = nbasis // 2
    assert (N * 2 == nbasis)
    M = np.ones((N, N), dtype='complex')
    spm = pauli_dict[i]
    return np.block([[M * spm[0, 0], M * spm[0, 1]],
                     [M * spm[1, 0], M * spm[1, 1]]])


def pauli_decomp(M):
    """ Given a 2*2 matrix, get the I, x, y, z component.
    :param M: 2*2 matrix
    :returns:  (I, x, y, z) are four scalars.
    :rtype: same as dtype of M
    """
    return (np.trace(s0.dot(M)) / 2, np.trace(s1.dot(M)) / 2,
            np.trace(s2.dot(M)) / 2, np.trace(s3.dot(M)) / 2)


def pauli_decomp2(M):
    """ Given a 2*2 matrix, get the I, x, y, z component. (method2)
    :param M: 2*2 matrix
    :returns:  (I, x, y, z) are four scalars.
    :rtype: same as dtype of M
    """
    return (np.sum(M * s0T) / 2, np.sum(M * s1T) / 2, np.sum(M * s2T) / 2,
            np.sum(M * s3T) / 2)


def pauli_sigma_norm(M):
    MI, Mx, My, Mz = pauli_decomp2(M)
    return np.linalg.norm([Mx, My, Mz])


def pauli_block_I(M, norb):
    """
    I compoenent of a matrix, see pauli_block
    """
    ret = zeros_like(M)
    tmp = (M[:norb, :norb] + M[norb:, norb:]) / 2
    ret[:norb, :norb] = ret[norb:, norb:] = tmp
    return ret


def pauli_block_x(M, norb):
    """
    x compoenent of a matrix, see pauli_block
    """
    ret = zeros_like(M)
    tmp = (M[:norb, norb:] + M[norb:, :norb]) / 2
    ret[:norb, norb:] = ret[norb:, :norb] = tmp
    return ret


def pauli_block_y(M, norb):
    """
    y compoenent of a matrix, see pauli_block
    """
    ret = zeros_like(M)
    tmp = (M[:norb, norb:] * 1j + M[norb:, :norb] * (-1j)) / 2
    ret[:norb, norb:] = tmp * (-1j)
    ret[norb:, :norb] = tmp * 1j
    return tmp, ret


def pauli_block_z(M, norb):
    """ z compoenent of a matrix, see pauli_block
    :param M:
    :param norb:
    :returns:
    :rtype:
    """
    ret = zeros_like(M)
    tmp = (M[:norb, :norb] - M[norb:, norb:]) / 2
    ret[:norb, :norb] = tmp
    ret[norb:, norb:] = -tmp
    return tmp, ret


def pauli_block(M, idim):
    """ Get the I, x, y, z component of a matrix.
    :param M: The input matrix,  aranged in four blocks:
    [[upup, updn], [dnup, dndn]]. let norb be number of orbitals in
    each block. (so M has dim 2norb1*2norb2)
    :param idim: 0, 1,2, 3 for I , x, y, z.
    :returns:  the idim(th) component of M
    :rtype: a matrix with shape of M.shape//2
    """
    # ret = zeros_like(M)
    norb1, norb2 = M.shape // 2
    if idim == 0:
        tmp = (M[:norb1, :norb2] + M[norb1:, norb2:]) / 2.0
    elif idim == 1:
        tmp = (M[:norb1, norb2:] + M[norb1:, :norb2]) / 2.0
    elif idim == 2:
        tmp = (M[:norb1, norb2:] * 1j + M[norb1:, :norb2] * (-1j)) / 2.0
    elif idim == 3:
        tmp = (M[:norb1, :norb2] - M[norb1:, norb2:]) / 2.0
    else:
        raise NotImplementedError()
    return tmp


def pauli_block_all(M):
    norb1, norb2 = np.array(M.shape) // 2
    MI = (M[:norb1, :norb2] + M[norb1:, norb2:]) / 2
    Mx = (M[:norb1, norb2:] + M[norb1:, :norb2]) / 2
    My = (M[:norb1, norb2:] * 1j + M[norb1:, :norb2] * (-1j)) / 2
    Mz = (M[:norb1, :norb2] - M[norb1:, norb2:]) / 2
    return MI, Mx, My, Mz


def pauli_block_sigma_norm(M):
    """
    M= MI * I + \vec{P} dot \vec{sigma}
    = MI*I + p * \vec{e} dot \vec{sigma}
    where p is the norm of P.
    """
    MI, Mx, My, Mz = pauli_block_all(M)
    #nMx = np.linalg.norm(Mx)
    #nMy = np.linalg.norm(My)
    #nMz = np.linalg.norm(Mz)
    #nM = np.sqrt(np.sum((nMx, nMy, nMz)))
    return (Mz) * np.sign(np.trace(Mz))