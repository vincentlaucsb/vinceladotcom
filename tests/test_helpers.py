from vinceladotcom.pages.forms import parse_metadata, deserialize_metadata
import vinceladotcom as site
import pytest

def test_title_to_url():
    from vinceladotcom.database import title_to_url
    
    assert(
        title_to_url('Why C++ is the Greatest Language Ever') ==
        'why-cpp-is-the-greatest-language-ever'
    )
    
    assert(
        title_to_url('Should people who wear crocs be allowed to vote?') ==
        'should-people-who-wear-crocs-be-allowed-to-vote'
    )

def test_parse_metadata():
    import json
    meta = ("Description: My dank article\n"
        "og:type: Article")
        
    expected = {
        'Description': 'My dank article',
        'og:type': 'Article'
    }
    
    assert parse_metadata(meta) == json.dumps(expected)
    
def test_deserialize_metadata():
    import json
    meta = json.dumps({
        "Description": "My dank article",
        "og:type": "Article"
    })
    
    assert deserialize_metadata(meta) == (
        "Description: My dank article\n"
        "og:type: Article\n"
    )