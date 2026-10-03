"""Módulo 13 - planejando endereços de rede (CIDR) com o módulo ipaddress.

Ao desenhar uma rede na nuvem (uma VPC/VNet com sub-redes), as perguntas
são sempre as mesmas: quantos endereços cabem? como dividir em sub-redes?
duas redes se sobrepõem? este IP pertence a esta sub-rede?

Fontes:
- https://docs.python.org/pt-br/3/library/ipaddress.html
- https://docs.python.org/pt-br/3/howto/ipaddress.html
"""

import ipaddress
from itertools import combinations

Rede = ipaddress.IPv4Network | ipaddress.IPv6Network


def descrever(cidr: str) -> str:
    """Um resumo de uma rede: quantos endereços, máscara, primeiro e último endereço."""
    rede = ipaddress.ip_network(cidr)
    return (
        f"{rede}: {rede.num_addresses} endereços, máscara {rede.netmask}, "
        f"de {rede.network_address} a {rede.broadcast_address}"
    )


def dividir(cidr: str, novo_prefixo: int) -> list[Rede]:
    """Divide uma rede em sub-redes do tamanho ``/novo_prefixo``."""
    return list(ipaddress.ip_network(cidr).subnets(new_prefix=novo_prefixo))


def sobreposicoes(cidrs: list[str]) -> list[tuple[str, str]]:
    """Os pares de redes que se sobrepõem (um conflito ao conectar redes)."""
    redes = [ipaddress.ip_network(cidr) for cidr in cidrs]
    return [
        (str(a), str(b))
        for a, b in combinations(redes, 2)
        if a.version == b.version and a.overlaps(b)
    ]


def pertence(ip: str, cidr: str) -> bool:
    """True se o endereço ``ip`` está dentro da rede ``cidr``."""
    return ipaddress.ip_address(ip) in ipaddress.ip_network(cidr)


def main() -> None:
    print(descrever("10.0.0.0/16"))
    print(descrever("10.0.1.0/24"))

    sub_redes = dividir("10.0.0.0/16", 24)
    print(f"10.0.0.0/16 em /24: {len(sub_redes)} sub-redes; as 3 primeiras:")
    for sub_rede in sub_redes[:3]:
        print(" ", sub_rede)
    print("em 4 partes iguais:", [str(rede) for rede in dividir("10.0.0.0/16", 18)])

    print(sobreposicoes(["10.0.0.0/16", "10.1.0.0/16", "10.0.128.0/17"]))
    print("10.0.3.7 em 10.0.0.0/22?", pertence("10.0.3.7", "10.0.0.0/22"))
    print("10.0.4.1 em 10.0.0.0/22?", pertence("10.0.4.1", "10.0.0.0/22"))
    print(descrever("2001:db8::/64"))  # IPv6 também funciona


if __name__ == "__main__":
    main()
