<tr>
                                <td class="li-product-remove"><a
                                        href="{% url 'frontRemoveItemFromWishlist' username=request.user.username pk=item.pk %}"><i
                                        class="fas fa-times-circle"></i></a></td>
                                <td class="li-product-thumbnail"><a
                                        href="/fe/product/details/{{item.product.product_id}}"><img
                                        src="{{item.product.productImg.first.img_link}}" style="width: 80px; height: 80px;"
                                        alt=""></a></td>
                                <td class="li-product-name"><a href="/fe/product/details/{{item.product.product_id}}">{{item.product.title|striptags|truncatechars:30}}</a>
                                </td>
                                <td class="li-product-price"><span class="amount">${{item.product.new_price}}</span>
                                </td>
                                {% if item.product.in_stock %}
                                <td class="li-product-stock-status"><span class="in-stock">In stock</span></td>
                                {% else %}
                                <td class="li-product-stock-status"><span class="in-stock">Out of stock</span></td>
                                {% endif %}
                                <td class="li-product-add-cart"><a
                                        href="{% url 'frontAddToCart' product_id=item.product.product_id %}">add to
                                    cart</a></td>
                            </tr>