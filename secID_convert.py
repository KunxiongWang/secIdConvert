#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author: wangkunxiong
@File: secID_convert.py
@Description: convert security IDs among different datasource
'''


class secIdSource(object):
    TYPE = ['etf', 'stock', 'index']
    SOURCE = ['ticker', 'tonglian', 'rq', 'wind', 'jq']
    EXCHANGE = ['shanghai', 'shenzhen']

    def to_ticker(self):
        raise NotImplemented

    def convert(self):
        raise NotImplemented


class ticker(secIdSource):
    """Security ID type is ticker

    Attributes:
        to_source: secIdSource.SOURCE the target source to convert
    """

    def __init__(self, to_source: secIdSource.SOURCE):
        self.to_source = to_source

    def convert(self, sec_id: str, sec_type: secIdSource.TYPE):
        """convert ticker ID into a specific sourse ID

        Args:
            sec_id: str, must be a ticker ID
            sec_type: secIdSource.TYPE, the type of security

        Returns:
            str, target source ID
        """
        if self.to_source == 'tonglian':
            if sec_type == 'etf':
                return self.etf_convert_tonglian(sec_id)
            else:
                raise ValueError(f'{sec_type} is not included so far')
        else:
            raise ValueError(f'{self.to_source} is not included so far')

    def etf_convert_tonglian(self, sec_id):
        """ etf ticker into tonglian ID

        Args:
            sec_id: str

        Returns:
            str, tonglian etf ID
        """
        if sec_id.startswith('15'):
            convert_id = sec_id + '.XSHE'
        elif sec_id.startswith(('51', '56', '58')):
            convert_id = sec_id + '.XSHG'
        else:
            print(f'{sec_id} is not named under rules, converted into {sec_id}.UKNOW')
            convert_id = sec_id + '.UKNOW'
        return convert_id


class tonglian(secIdSource):
    """Security ID type is tonglian

    Attributes:
        to_source: secIdSource.SOURCE the target source to convert
    """

    def __init__(self, to_source: secIdSource.SOURCE):
        self.to_source = to_source

    def to_ticker(self, tonglian_id: str, sec_type: secIdSource.TYPE):
        """convert tonglian ID into ticker ID

        Args:
            tonglian_id: str
            sec_type: secIdSource.TYPE

        Returns:
            str, ticker ID

        """
        if sec_type == 'etf':
            return self.etf_to_ticker(tonglian_id)
        else:
            raise ValueError(f'{sec_type} is not included so far')

    def convert(self, tonglian_id: str, sec_type: secIdSource.TYPE):
        """convert tonglian ID into a specific source ID

        Args:
            tonglian_id: str
            sec_type: secIdSource.TYPE

        Returns:
            str, spicific source ID

        """
        if self.to_source == 'ticker':
            ticker_id = self.to_ticker(tonglian_id, sec_type)
            conveted_id = ticker_id
            return conveted_id
        raise ValueError(f'{self.to_source} is not included so far')

    def etf_to_ticker(self, tonglian_etf_id: str):
        """convert tonglian etf ID to ticker

        Args:
            tonglian_etf_id: str

        Returns:
            str, ticker ID
        """
        if any(x in tonglian_etf_id for x in ['XSHG', 'XSHE']):
            ticker_id = tonglian_etf_id.split('.')[0]
        else:
            print(f'{tonglian_etf_id} is not named under rules, converted into {tonglian_etf_id}.UKNOW')
            ticker_id = tonglian_etf_id + '.UKNOW'
        return ticker_id


if __name__ == '__main__':

    test_ticker_list = ['151001', '510124', 'HXI224']
    id_source = ticker(to_source='tonglian')
    convert_dict = {}
    for i in test_ticker_list:
        convert_dict[i] = id_source.convert(i, 'etf')
    print(convert_dict)

    test_tonglian_list = list(convert_dict.values())
    id_source = tonglian(to_source='ticker')
    convert_dict = {}
    for i in test_tonglian_list:
        convert_dict[i] = id_source.convert(i, 'etf')
    print(convert_dict)
